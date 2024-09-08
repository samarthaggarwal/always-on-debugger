import re
from typing import Dict, Any

from llm import AnthropicLLM, Conversation

class Debugger:
    DELIMITER = "#######"
    SYSTEM_PROMPT = f"""
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

    def generate_user_prompt(self, error: str, code_snippet: str) -> str:
        return f"""
        Here is the error message and relevant code:
        
        ===============
        <error>
        {error}
        </error>
        <code_snippet>
        {code_snippet}
        </code_snippet>
        ===============
        """

    def debug(self, error: str, code_snippet: str) -> Dict[str, Any]:
        user_prompt = self.generate_user_prompt(error, code_snippet)
        conversation = Conversation()
        conversation.add_user_message(user_prompt)
        messages = conversation.to_dict()
        
        llm_response = self.llm.generate_conversation_stream_print(self.SYSTEM_PROMPT, messages, model="latest_large")
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
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, llm_response, re.DOTALL)
                result[key] = match.group(1).strip() if match else ""
            
            return result
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {}