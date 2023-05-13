from typing import List

from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import SystemMessage

assignment_template = """Please evaluate student assignment according to criteria I will give you. Format the output as markdown.
 Here are the criteria:
    {criteria}
    
    Rest is the student assignment:
    {assignment}
"""

assignment_human: HumanMessagePromptTemplate = HumanMessagePromptTemplate.from_template(assignment_template)


def setup_chat():
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            content="You are AI assistant teacher, that evaluates student assignments according to criteria"),
        assignment_human
    ])
    return prompt
