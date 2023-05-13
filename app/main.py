from langchain import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredPDFLoader

from app.evaluation_chat import setup_chat
from app.streaming_file import StreamingFileCallbackHandler

# llm = OpenAI(temperature=0, model_name="gpt-4", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
chat = ChatOpenAI(temperature=0, model_name="gpt-4", streaming=True,
                  callbacks=[StreamingStdOutCallbackHandler(), StreamingFileCallbackHandler("output/evaluation.md")])


def main():
    file_location = "test_input/single_document/Physics_IA.pdf"
    loader = UnstructuredPDFLoader(file_location)
    assignment_docs = loader.load()
    assignment = [doc.page_content for doc in assignment_docs]
    print("\n\n".join(assignment))
    with open("criteria/ib_marking_rubic.txt") as f:
        criteria_text = f.read()
    prompt = setup_chat()
    chain = LLMChain(llm=chat, prompt=prompt)
    chain.run(criteria=criteria_text, assignment=assignment)


if __name__ == '__main__':
    main()
