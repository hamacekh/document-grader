import tempfile

from langchain import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredPDFLoader
import streamlit as st

from streaming_widget import StreamingWidgetCallbackHandler
from evaluation_chat import setup_chat
from streaming_file import StreamingFileCallbackHandler

st.title("Student assignment evaluation")

# llm = OpenAI(temperature=0, model_name="gpt-4", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])

def add_download_button(filename: str):
    with open(filename, "r") as f:
        data = f.read()
        st.download_button(
            label="Download output as file",
            data=data,
            file_name="ai_assesment.md",
            mime="text/markdown"
        )

def main():
    st.header("Input")
    student_file = st.file_uploader(label="Upload student pdf assignment", type="pdf")
    evaluation_criteria = st.file_uploader(label="Upload evaluation criteria as text file", type=["html", "md", "txt"])
    if student_file is None or evaluation_criteria is None:
        st.write("Pick student file and evaluation criteria")
    else:
        st.header("Output")
        output_widget = st.empty()
        chat = ChatOpenAI(temperature=0, model_name="gpt-4", streaming=True,
                          callbacks=[StreamingStdOutCallbackHandler(),
                                     StreamingFileCallbackHandler(
                                         "output/evaluation.md",
                                         on_finish=add_download_button),
                                     StreamingWidgetCallbackHandler(output_widget)
                                     ])
        with tempfile.NamedTemporaryFile(suffix=".pdf") as fp:
            fp.write(student_file.getvalue())
            temp_path = fp.name
            loader = UnstructuredPDFLoader(temp_path)
            assignment_docs = loader.load()
        assignment = [doc.page_content for doc in assignment_docs]
        print("\n\n".join(assignment))
        criteria_text = evaluation_criteria.getvalue().decode("utf-8")
        prompt = setup_chat()
        chain = LLMChain(llm=chat, prompt=prompt)
        chain.run(criteria=criteria_text, assignment=assignment)


if __name__ == '__main__':
    main()
