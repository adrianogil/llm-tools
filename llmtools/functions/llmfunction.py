
class LLMFunction:
    def get_function_name(self):
        return "function_name"

    def get_function_metadata(self):
        return {
            "name": "function_name",
            "description": "function description",
            "parameters": "parameters"
        }

    def run_function(self, llmassistant, arguments):
        pass
