from typing import Union, Callable, List

from swarm import Agent
from swarm.types import AgentFunction


def transfer_to_validation_agent():
    """Transfer spanish speaking users immediately."""
    return validation_agent


def transfer_to_form_agent():
    """Transfer spanish speaking users immediately."""
    return form_agent


def transfer_to_approval_agent():
    return approval_agent


class ValidationAgent(Agent):
    name: str = "Validation Agent"
    model: str = "gpt-4o-mini"
    instructions: Union[str, Callable[[], str]] = """
    You are a customer data validation agent. 
    You can validate each field provided by the user for correct email format, phone format, etc.
    If you find some errors in the form, you can ask the user to correct them and transfer to form agent.
    If all data looks valid and the user chose business, submit the form to business agent immediately otherwise to personal agent.
"""
    functions: List[AgentFunction] = [
        transfer_to_approval_agent, transfer_to_form_agent]


class FormAgent(Agent):
    name: str = "Form Agent"
    model: str = "gpt-4o-mini"
    instructions: Union[str, Callable[[], str]] = """
    You are a form filling agent. You can help users fill out form for loan.
    Ask for the user's name, email, phone number, is he a BOC customer or not and the purpose of the loan personal or business.
    After all fields are filled, submit the form to validation agent.
"""
    functions: List[AgentFunction] = [transfer_to_validation_agent]


class InfoAgent(Agent):
    name: str = "Information Agent"
    model: str = "gpt-4o-mini"
    instructions: Union[str, Callable[[], str]] = """
    You are a loan information agent. 
    You can answer questions about loans, terms, and interest rates.
    If user asks to apply for loan, transfer to form agent.
    """
    functions: List[AgentFunction] = [transfer_to_form_agent]


class ApprovalAgent(Agent):
    name: str = "Approval Agent"
    model: str = "gpt-4o-mini"
    instructions: Union[str, Callable[[], str]] = """
    You are a loan approval agent. 
    You can approve or reject the loan application.
    Approve the loan application if all data is correct and valid, loan amount is within limits, etc.
    If you reject the loan, you can ask the user to correct the form and transfer to form agent.
    If you approve the loan, you can ask the user to confirm the loan and transfer to validation agent.
    """
    functions: List[AgentFunction] = [transfer_to_validation_agent, transfer_to_form_agent]


info_agent = InfoAgent()
form_agent = FormAgent()
validation_agent = ValidationAgent()
approval_agent = ApprovalAgent()

agent = info_agent

all_agents = {
    info_agent.name: info_agent,
    form_agent.name: form_agent,
    validation_agent.name: validation_agent,
    approval_agent.name: approval_agent,
}
