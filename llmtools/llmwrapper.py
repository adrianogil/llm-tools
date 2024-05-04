import llm
import os


def get_llm_output(prompt, model='claude-3-haiku'):
    llm_model = llm.get_model(model)
    if model.startswith('claude-'):
        llm_model.key = os.environ["CLAUDE_API_KEY"]
    else:
        llm_model.key = os.environ["CHATGPT_API_KEY"]
    response = llm_model.prompt(prompt)
    return response.text()
