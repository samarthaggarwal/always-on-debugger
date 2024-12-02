import re
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv, find_dotenv
from typing import Callable, Dict, List, Optional

import openai
import anthropic

# Environment setup
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

from aidebug.llm import AnthropicLLM, Conversation

class Debugger:
    DELIMITER = "#######"
    FILE_DETECTION_SYSTEM_PROMPT = f"""
    You are an experienced engineer who is helping a junior engineer to debug the error.

    {DELIMITER} Instruction:
    - Carefully read the command run by the user and the resulting error.
    - Identify if the error is related to a specific file. If so, return the file path. If not, return NO_FILE.

    {DELIMITER} Output:
    <filepath>
    {{Just return the file path as a string. If not related to any file, return NO_FILE. Do not add any other information.}}
    </filepath>
    """

    DEBUG_SYSTEM_PROMPT = f"""
    You are an experienced engineer who is helping a junior engineer to debug the error.

    {DELIMITER} Instruction:
    - Carefully read the user's input that includes error and optionally code snippet.
    - Generate a list of hypotheses to explain the error.
    - Then suggest clear and concise steps users can follow to validate the error

    {DELIMITER}: Output
    <thinking>
    {{Present your thinking and approach here}}
    </thinking>
    <recommendation>
    {{Present your recommendation here. Be very specific, concise and actionable.}}
    </recommendation>
    """
    # <reflection>
    # {{Present your reflection on the recommendation here. If you think the recommendation is not enough, suggest more information you may need to solve the problem.}}
    # </reflection>

    def __init__(self):
        self.llm = AnthropicLLM()
        self.llm.client.api_key = os.environ.get("ANTHROPIC_API_KEY")
        #print(f"Anthropic API key: {self.llm.client.api_key}")

    def generate_user_prompt_for_file_detection(self, command: str, error: str) -> str:
        return f"""
        Here is the command and error message:
        ===============
        <command>
        {command}
        </command>
        <error>
        {error}
        </error>
        """

    def detect_file_path(self, command: str, error: str) -> Optional[str]:
        user_prompt = self.generate_user_prompt_for_file_detection(command, error)
        conversation = Conversation()
        conversation.add_user_message(user_prompt)
        messages = conversation.to_dict()

        llm_response = self.llm.generate_conversation(self.FILE_DETECTION_SYSTEM_PROMPT, messages, model="small")
        parsed_response = self.parse_response(llm_response)
        filepath = parsed_response["filepath"]
        if filepath == "NO_FILE":
            return None
        return filepath

    def generate_user_prompt_for_debug(self, command: str, error: str, code_snippet: Optional[str]) -> str:
        if code_snippet is None:
            return f"""
            Here is the command and error message:
            ===============
            <command>
            {command}
            </command>
            <error>
            {error}
            </error>
            """
        else:
            return f"""
            Here is the command, error message and relevant code:
            ===============
            <command>
            {command}
            </command>
            <error>
            {error}
            </error>
            <code_snippet>
            {code_snippet}
            </code_snippet>
            ===============
            """

    def debug(self, command: str, error: str, code_snippet: Optional[str] = None) -> Dict[str, Any]:
        user_prompt = self.generate_user_prompt_for_debug(command, error, code_snippet)
        conversation = Conversation()
        conversation.add_user_message(user_prompt)
        messages = conversation.to_dict()

        llm_response = self.llm.generate_conversation_stream_print(self.DEBUG_SYSTEM_PROMPT, messages, model="latest_large")
        parsed_response = self.parse_response(llm_response)
        
        return parsed_response

    @staticmethod
    def parse_response(llm_response: str) -> Dict[str, Any]:
        """
        Parse an XML-like string LLM response to get structured output using regex.
        """
        try:
            result = {}
            
            patterns = {
                'thinking': r'<thinking>(.*?)</thinking>',
                'recommendation': r'<recommendation>(.*?)</recommendation>',
                # 'reflection': r'<reflection>(.*?)</reflection>'
                'filepath': r'<filepath>(.*?)</filepath>'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, llm_response, re.DOTALL)
                result[key] = match.group(1).strip() if match else ""
            
            return result
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {}