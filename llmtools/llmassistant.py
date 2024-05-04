from llmtools.functions.outputmessagefunction import OutputMessageLLMFunction
from llmtools.functions.runcommandfunction import RunCommandLLMFunction
from llmtools.functions.createfilefunction import CreateFileLLMFunction
from llmtools.basic.promptinput import get_user_input

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["CHATGPT_API_KEY"],
)

def get_chatgpt_output(user_input="Hello world!", messages=None, functions=None):
    if not messages:
        messages = []
    messages.append({"role": "user", "content": user_input})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    return completion


class LLMAssistant:
    def __init__(self):
        self.functions = [
            OutputMessageLLMFunction(),
            RunCommandLLMFunction(),
            CreateFileLLMFunction(),
        ]
        self.is_chat_running = False
        self.debug_mode = False

    def get_functions(self):
        llm_functions = []
        for registered_function in self.functions:
            llm_functions.append(registered_function.get_function_metadata())
        return llm_functions

    def run_prompt(self, prompt):
        if self.debug_mode:
            print("Running prompt: " + str(prompt))
        chatgpt_functions = self.get_functions()
        if self.debug_mode:
            print(chatgpt_functions)
        self.last_completion = get_chatgpt_output(user_input=prompt, functions=chatgpt_functions)
        if self.last_completion.choices[0].message.function_call is None:
            print(self.last_completion.choices[0].message.content)
        else:
            target_function_call = self.last_completion.choices[0].message.function_call.name
            for function in self.functions:
                if function.get_function_name() == target_function_call:
                    function.run_function(self, self.last_completion.choices[0].message.function_call.arguments)
                    break
            else:
                print("Function not found: " + str(target_function_call))

    def run(self):
        self.is_chat_running = True
        while self.is_chat_running:
            prompt_message_to_user = self.get_prompt_message_to_user()
            prompt = get_user_input(prompt_message_to_user)
            prompt = prompt.strip()
            if self.verify_prompt(prompt):
                prompt = self.postprocess_prompt(prompt)
                self.run_prompt(prompt)

    def postprocess_prompt(self, prompt):
        return prompt

    def get_prompt_message_to_user(self):
        return "User: "

    def verify_prompt(self, prompt):
        if prompt == "debug":
            import pdb; pdb.set_trace()
            return False
        if prompt in ["exit", "quit", "finish", "q"]:
            print("Exiting chat.")
            self.is_chat_running = False
            return False
        return True


if __name__ == "__main__":
    assistant = LLMAssistant()
    assistant.run()
