from .llmfunction import LLMFunction

from pydantic import BaseModel, Field
import json


class OutputMessageToUser(BaseModel):
    message: str = Field(..., description="The message to show to the user")


class OutputMessageLLMFunction(LLMFunction):

    def get_function_name(self):
        return "output_message_to_user"

    def get_function_metadata(self):
        return {
            "name": self.get_function_name(),
            "description": "Output a message to the user",
            "parameters": OutputMessageToUser.schema(),
        }

    def run_function(self, llmassistant, arguments):
        output_message_data = OutputMessageToUser(**json.loads(arguments))
        print(output_message_data.message)
