# Related third-party imports
import abc
import os
import logging
import tiktoken
from dotenv import load_dotenv, find_dotenv
from typing import Callable, Dict, List, Optional

import openai
import anthropic
# Environment setup
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_KEY"]


MODEL_MAPPING = {
    "openai": {
        "small": "gpt-3.5-turbo-0125",
        "medium": "gpt-4",
        "large": "gpt-4-turbo",
        "latest_large": "gpt-4o"
    },
    "anthropic": {
        "small": "claude-3-haiku-20240307",
        "medium": "claude-3-sonnet-20240229",
        "large": "claude-3-opus-20240229", 
        "latest_large": "claude-3-5-sonnet-20240620"
    }
}

class LLM(abc.ABC):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    @abc.abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        pass

    @abc.abstractmethod
    def stream_text(self, prompt: str, **kwargs):
        pass

class OpenAILLM(LLM):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or OPENAI_API_KEY)
        self.client = openai.OpenAI(api_key=self.api_key)

    def generate_text(self, prompt: str, model: str = "large", **kwargs) -> str:
        model_name = MODEL_MAPPING["openai"][model]
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=kwargs.get("temperature", 0.2),
        )
        logger.info(f"Response from OpenAI: {response.choices[0].message.content}")
        return response.choices[0].message.content
    
    def stream_text(self, prompt: str, model: str = "large", **kwargs):
        model_name = MODEL_MAPPING["openai"][model]
        messages = [{"role": "user", "content": prompt}]
        stream = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=kwargs.get("temperature", 0.2),
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].message['content'] is not None:
                yield chunk.choices[0].message['content']

    def generate_conversation(self, messages, model: str = "large", **kwargs) -> str:
        model_name = MODEL_MAPPING["openai"][model]
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=kwargs.get("temperature", 0.2),
        )
        logger.info(f"Response from OpenAI: {response.choices[0].message.content}")
        return response.choices[0].message.content
    
    def generate_conversation_stream(self, messages, model: str = "large", **kwargs):
        model_name = MODEL_MAPPING["openai"][model]
        stream = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=kwargs.get("temperature", 0.2),
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response_string = chunk.choices[0].delta.content
                yield response_string


class AnthropicLLM(LLM):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or ANTHROPIC_API_KEY)
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_text(self, prompt: str, model: str = "large", **kwargs) -> str:
        model_name = MODEL_MAPPING["anthropic"][model]
        response = self.client.messages.create(
            model=model_name,
            temperature=kwargs.get("temperature", 0.0),
            max_tokens=kwargs.get("max_tokens", 4096),
            messages=[{"role": "user", "content": prompt}]
        )
        logger.info(f"Response from Anthropic: {response.content[0].text}")
        return response.content[0].text

    def generate_conversation(self, system_message, messages, model: str = "large", **kwargs) -> str:
        model_name = MODEL_MAPPING["anthropic"][model]
        system = system_message
        response = self.client.messages.create(
            model=model_name,
            system=system,
            temperature=kwargs.get("temperature", 0.0),
            max_tokens=kwargs.get("max_tokens", 4096),
            messages=messages
        )
        logger.info(f"Response from Anthropic: {response.content[0].text}")
        return response.content[0].text

    def stream_text(self, prompt: str, model: str = "large", **kwargs):
        model_name = MODEL_MAPPING["anthropic"][model]
        messages = [{"role": "user", "content": prompt}]
        with self.client.messages.stream(
            model=model_name,
            temperature=kwargs.get("temperature", 0.0),
            max_tokens=kwargs.get("max_tokens", 4096),
            messages=messages,
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk
    
    def generate_conversation_stream(self, system_message, messages, model: str = "large", **kwargs):
        model_name = MODEL_MAPPING["anthropic"][model]
        system = system_message
        with self.client.messages.stream(
            system=system,
            model=model_name,
            temperature=kwargs.get("temperature", 0.0),
            max_tokens=kwargs.get("max_tokens", 4096),
            messages=messages,
        ) as stream:
            for chunk in stream.text_stream:
                if chunk is not None:
                    yield chunk
    
    def generate_conversation_stream_print(self, system_message, messages, model: str = "large", **kwargs):
        model_name = MODEL_MAPPING["anthropic"][model]
        system = system_message
        response = ""
        with self.client.messages.stream(
            system=system,
            model=model_name,
            temperature=kwargs.get("temperature", 0.0),
            max_tokens=kwargs.get("max_tokens", 4096),
            messages=messages,
        ) as stream:
            for chunk in stream.text_stream:
                if chunk is not None:
                    response += chunk
                    # print(chunk, end="", flush=True)
        return response

class Message:
    def __init__(
        self,
        role: str,
        content: str,
        name: str = None,
    ):
        self.role = role
        self.content = content
        self.name = name

    def to_dict(self):
        message_dict = {"role": self.role, "content": self.content}
        if self.name:
            message_dict["name"] = self.name
        return message_dict

class Conversation:
    def __init__(self, system_message=None):
        self.messages = []
        if system_message:
            self.messages.append(Message(role="system", content=system_message))

    def __iter__(self):
        for message in self.messages:
            yield message

    def to_dict(self):
        return [message.to_dict() for message in self.messages]

    def add_message(self, message: Dict[str, str]):
        self.messages.append(Message(**message))

    def add_user_message(self, question: str):
        self.add_message({"role": "user", "content": question})

    def add_assistant_message(self, answer: str):
        self.add_message({"role": "assistant", "content": answer})

    def print_conversation(self):
        for message in self.messages:
            logger.info(f"{message.role}: {message.content}")