from typing import List

from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import SystemMessage

assignment_template = """Please evaluate student submission according to criteria I will give you.
Format the output as markdown.
 Here are the criteria:
    {criteria}
    
    Rest is the student submission:
    {assignment}
"""

assignment_human: HumanMessagePromptTemplate = HumanMessagePromptTemplate.from_template(assignment_template)


def setup_chat():
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            content="You are AI assistant teacher, that evaluates student submissions according to criteria."
                    "You always include final grade or point summary in your evaluation, depending on what"
                    "is applicable for the requested evaluation criteria."
                    "You must not give non integral amount of points if not otherwise specified in the criteria."),
        assignment_human
    ])
    return prompt
