from .llmfunction import LLMFunction

from pydantic import BaseModel, Field
from typing import List
import json


class SingleActionPlan(BaseModel):
    """
    A single action to be executed in a multi-step plan.
    """
    prompt: str = Field(..., description="The message to show to the user")

class EvaluateActionPlanResult(BaseModel):
    """
    The result of evaluating an action in a multi-step plan.
    """
    action: SingleActionPlan = Field(..., description="The action to evaluate")
    result: str = Field(..., description="The result of the evaluation")


class RequestMultiStepPlan(BaseModel):
    """
    Start the creation of a multi-step plan in case the user request is too complex.
    """
    stepsToExecute: List[SingleActionPlan] = Field(..., description="The steps to execute")


class MultiStepPlanLLMFunction(LLMFunction):

    def get_function_name(self):
        return "multistep_plan"

    def get_function_metadata(self):
        return {
            "name": self.get_function_name(),
            "description":
            """Executes a multi-step plan by running each step as a separate prompt.
            This function should be used in case user ask for a complex request that
            requires multiple steps to be executed.""",
            "parameters": RequestMultiStepPlan.schema(),
        }

    def run_function(self, llmassistant, arguments):
        request_plan_data = RequestMultiStepPlan(**json.loads(arguments))
        results = []

        # Debug
        print("Running multi-step plan with the following steps:")
        for i, step in enumerate(request_plan_data.stepsToExecute):
            print(i, " - ", step.prompt)

        for step in request_plan_data.stepsToExecute:
            # Run each step's prompt using the LLM assistant's run_prompt method
            llmassistant.run_prompt(step.prompt)

        return results
