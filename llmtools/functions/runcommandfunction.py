from .llmfunction import LLMFunction

from pyutils.utils.userinput import get_user_input
from pyutils.cli.clitools import run_cmd
from pydantic import BaseModel, Field

import platform
import json
import os
import random


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

        def save_command_to_file(command):
            file_path = "/temp/command.sh"
            file_name = f"command_{random.randint(1, 100)}.sh"
            file_path = os.path.join("/temp", file_name)
            with open(file_path, "w") as file:
                file.write(command)
            print(f"Command saved to file: {file_path}")

        save_command_to_file(run_command_data.command)

        user_confirmation = get_user_input("Do you want to run this command? (y/n): ").strip()

        if user_confirmation.lower() == "y":
            print(f"> {run_command_data.command}")
            cmd_ouput = run_cmd(run_command_data.command)
            print(cmd_ouput)
            print("Command ran successfully")
        else:
            print("Operation canceled")
