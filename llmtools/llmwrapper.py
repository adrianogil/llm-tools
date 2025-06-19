import os

claude_model_name = 'claude-3-haiku-20240307'
chatgpt_model_name = 'gpt-4o-mini'

def get_llm_output(prompt, model=chatgpt_model_name):
    import llm
    llm_model = llm.get_model(model)
    if model.startswith('claude-'):
        llm_model.key = os.environ["CLAUDE_API_KEY"]
    else:
        llm_model.key = os.environ["CHATGPT_API_KEY"]
    response = llm_model.prompt(prompt)
    return response.text()


class ChatGPTLLMModel:
    def __init__(self, model=chatgpt_model_name, key=None, project=None):

        self.model_name = model
        self.openai_key = key
        self.project = project

        self.prompt_messages = []

        if not self.openai_key:
            self.openai_key = os.environ["CHATGPT_API_KEY"]
        elif not self.openai_key.startswith("sk"):
            self.openai_key = os.environ[key]

        client_args = {
            "api_key": self.openai_key
        }
        if project:
            client_args["project"] = project

        from openai import OpenAI
        self.openai_client = OpenAI(**client_args)

    def run_prompt(self, prompt, should_keep_prompt_history=True):

        message = {
            "role": "user",
            "content": prompt
        }
        self.prompt_messages.append(message)

        prompt_args = {
            "input": self.prompt_messages,
            "model": self.model_name
        }
        response = self.openai_client.responses.create(**prompt_args)

        if not should_keep_prompt_history:
            self.prompt_messages = []
        else:
            self.prompt_messages.append({
                "role": "assistant",
                "content": response.output_text
            })

        return response.output_text

class LLMRunner:
    def __init__(self, model=chatgpt_model_name, **kwargs):
        self.model = model
        self.llm_model = None
        if model.startswith('gpt-'):
            self.llm_model = ChatGPTLLMModel(model=model, **kwargs)

    def run_prompt(self, prompt, **kwargs):
        response = self.llm_model.run_prompt(prompt, **kwargs)
        return response

