from typing import List

from langchain.prompts.chat import BaseStringMessagePromptTemplate
from langchain.schema import BaseMessage, AIMessage
from langchain.text_splitter import TextSplitter


def insert_between_items(original_list, item_to_insert):
    """
    Inserts a specified item between each item in the original list, leaving the original list items unchanged.

    Parameters:
    original_list (list): The original list of items.
    item_to_insert (str): The item to insert between each item in the original list.

    Returns:
    list: A new list with the specified item inserted between each item from the original list.

    Test Cases:
    >>> insert_between_items(["apple", "banana", "cherry", "date"], " ")
    ['apple', ' ', 'banana', ' ', 'cherry', ' ', 'date']

    >>> insert_between_items([1, 2, 3, 4], 0)
    [1, 0, 2, 0, 3, 0, 4]

    >>> insert_between_items(["a", "b"], ",")
    ['a', ',', 'b']

    >>> insert_between_items([], ",")
    []
    """
    if not original_list:  # If the list is empty, return an empty list
        return []

    # Add the specified item after each element except for the last one
    updated_list = [item for sublist in [(x, item_to_insert) for x in original_list[:-1]] for item in sublist] + [
        original_list[-1]]
    return updated_list


def text_chunks_to_chat(text_chunks: List[str], splitter: TextSplitter, template: BaseStringMessagePromptTemplate) -> List[BaseMessage]:
    text_splits = [chunk
                   for text in text_chunks
                   for chunk in splitter.split_text(text)]
    chat = \
        insert_between_items([template.format(text_part=chunk) for chunk in text_splits],
                             AIMessage(content="READ"))
    return chat
