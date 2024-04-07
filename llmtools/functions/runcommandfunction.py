from .llmfunction import LLMFunction

from llmtools.basic.promptinput import get_user_input

from pyutils.cli.clitools import run_cmd
from pydantic import BaseModel, Field

import platform
import json


class RunCommand(BaseModel):
    command: str = Field(..., description="The command to run")
    description: str = Field(..., description="The description of the command")


class RunCommandLLMFunction(LLMFunction):

    def get_function_name(self):
        return "run_command"

    def get_function_metadata(self):
        user_operational_system = platform.system()

        return {
            "name": self.get_function_name(),
            "description": "Run a command in the terminal. Consider user OS: " + user_operational_system,
            "parameters": RunCommand.schema(),
        }

    def run_function(self, llmassistant, arguments):
        run_command_data = RunCommand(**json.loads(arguments))

        print("Command to run:")
        print(run_command_data.command)
        print("Description:")
        print(run_command_data.description)

        user_confirmation = get_user_input("Do you want to run this command? (y/n): ")
        user_confirmation = user_confirmation.strip()

        if user_confirmation.lower() == "y":
            print(f"> {run_command_data.command}")
            cmd_ouput = run_cmd(run_command_data.command)
            print(cmd_ouput)
            print("Command ran successfully")
        else:
            print("Command not ran")
