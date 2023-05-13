from typing import List

from langchain import PromptTemplate, LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredPDFLoader
from pypdf import PdfReader

from app.evaluation_chat import setup_chat
from app.streaming_file import StreamingFileCallbackHandler

# llm = OpenAI(temperature=0, model_name="gpt-4", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
chat = ChatOpenAI(temperature=0, model_name="gpt-4", streaming=True,
                  callbacks=[StreamingStdOutCallbackHandler(), StreamingFileCallbackHandler("output/evaluation.md")])


# Function to convert PDF to markdown
def convert_pdf_to_text(file_path: str) -> List[str]:
    # Open the PDF file
    with open(file_path, "rb") as file:
        # Create a PDF file reader object
        pdf_reader = PdfReader(file_path)

        # Initialize an empty string to store the text
        text = []

        # Loop through each page in the PDF
        for page in pdf_reader.pages:
            # Extract the text from the page
            page_text = page.extract_text()

            # Add the text to the overall text
            text.append(page_text)

        return text


def convert_text_to_markdown(text: str) -> str:
    template = """Convert following text to markdown:
    
    {text}
    """
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template
    )
    return chat(prompt.format(text=text))


def main():
    file_location = "test_input/single_document/Physics_IA.pdf"
    loader = UnstructuredPDFLoader(file_location)
    assignment_docs = loader.load()
    assignment = [doc.page_content for doc in assignment_docs]
    print("\n\n".join(assignment))
    with open("criteria/ib_marking_rubic.txt") as f:
        criteria_text = f.read()
    prompt = setup_chat(assignment, criteria_text)
    chain = LLMChain(llm=chat, prompt=prompt)
    chain.run(criteria=criteria_text, assignment=assignment)


if __name__ == '__main__':
    main()
