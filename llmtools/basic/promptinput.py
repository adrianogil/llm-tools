from prompt_toolkit import PromptSession
prompt_session = PromptSession()

def get_user_input(user_prompt):
    return prompt_session.prompt(user_prompt)
