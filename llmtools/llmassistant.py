from llmtools.functions.outputmessagefunction import OutputMessageLLMFunction

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
        self.functions = [OutputMessageLLMFunction()]
        self.is_chat_running = False

    def get_functions(self):
        llm_functions = []
        for registered_function in self.functions:
            llm_functions.append(registered_function.get_function_metadata())
        return llm_functions

    def run_prompt(self, prompt):
        self.last_completion = get_chatgpt_output(user_input=prompt, functions=self.get_functions())
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
        from prompt_toolkit import PromptSession
        prompt_session = PromptSession()

        self.is_chat_running = True
        while self.is_chat_running:
            prompt_message_to_user = self.get_prompt_message_to_user()
            prompt = prompt_session.prompt(prompt_message_to_user)
            prompt = self.postprocess_prompt(prompt)
            if self.verify_prompt(prompt):
                self.run_prompt(prompt)

    def postprocess_prompt(self, prompt):
        return prompt.strip()

    def get_prompt_message_to_user(self):
        return "User: "

    def verify_prompt(self, prompt):
        if prompt == "debug":
            import pdb; pdb.set_trace()
            return True
        if prompt in ["exit", "quit", "finish"]:
            print("Exiting chat.")
            self.is_chat_running = False
            return False
        return True


if __name__ == "__main__":
    assistant = LLMAssistant()
    assistant.run()
