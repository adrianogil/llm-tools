from .llmfunction import LLMFunction

from pyutils.utils.userinput import get_user_input
from pydantic import BaseModel, Field

import platform
import json


class CreateFileCommand(BaseModel):
    # filePath: str = Field(..., description="The path of the file to create")
    fileName: str = Field(..., description="The name of the file to create")
    fileContent: str = Field(..., description="The content of the file to create")


class CreateFileLLMFunction(LLMFunction):

    def get_function_name(self):
        return "create_file"

    def get_function_metadata(self):
        user_operational_system = platform.system()

        return {
            "name": self.get_function_name(),
            "description": "Create a file. Consider user OS: " + user_operational_system,
            "parameters": CreateFileCommand.schema(),
        }

    def run_function(self, llmassistant, arguments):
        createfile_command_data = CreateFileCommand(**json.loads(arguments))

        consent = get_user_input(f"Do you want to create the file {createfile_command_data.fileName}? (y/n)")
        if consent.lower() != "y":
            print("Operation canceled")
            return

        with open(createfile_command_data.fileName, "w") as file:
            file.write(createfile_command_data.fileContent)
        print(f"File {createfile_command_data.fileName} created successfully")
