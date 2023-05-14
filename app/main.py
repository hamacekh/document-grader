import tempfile

import pypandoc
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredPDFLoader, UnstructuredFileLoader
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile

from evaluation_chat import setup_chat
from streaming_widget import StreamingWidgetCallbackHandler
from utils import get_filename_without_extension, get_file_extension

st.title("Student submission evaluation")


@st.cache_data
def uploaded_file_to_txt(uploaded: UploadedFile) -> str:
    extension = get_file_extension(uploaded.name)
    with tempfile.NamedTemporaryFile(suffix=f".{extension}") as fp:
        fp.write(uploaded.getvalue())
        temp_path = fp.name
        loader = UnstructuredFileLoader(temp_path)
        assignment_docs = loader.load()
    assignment = "\n\n".join([doc.page_content for doc in assignment_docs])
    return assignment


def execute_evaluation(student_text: str, criteria_text: str,
                       output_widget: DeltaGenerator) -> str:
    chat = ChatOpenAI(temperature=0, model_name="gpt-4", streaming=True,
                      callbacks=[StreamingWidgetCallbackHandler(output_widget)])
    prompt = setup_chat()
    chain = LLMChain(llm=chat, prompt=prompt)
    return chain.run(criteria=criteria_text, submission=student_text)


def main():
    st.header("Input")
    student_file = st.file_uploader(label="Upload student submission")
    with st.expander("Detected student submission content"):
        if student_file is None:
            st.write("No file uploaded")
        else:
            student_text = uploaded_file_to_txt(student_file)
            st.write(student_text)
    evaluation_criteria = st.file_uploader(label="Upload evaluation criteria")
    with st.expander("Detected evaluation criteria file content"):
        if evaluation_criteria is None:
            st.write("No file uploaded")
        else:
            evaluation_text = uploaded_file_to_txt(evaluation_criteria)
            st.write(evaluation_text)

    if student_file is None or evaluation_criteria is None:
        st.write("Pick student file and evaluation criteria")
    else:
        act = st.button("Evaluate")
        if act:
            st.header("Output")
            output_widget = st.empty()
            result_md = execute_evaluation(student_text, evaluation_text, output_widget)
            output_widget.markdown(result_md)
            student_file_basename = get_filename_without_extension(student_file.name)
            st.download_button(
                label="Download evaluation as markdown file",
                data=result_md,
                file_name=f"{student_file_basename}_evaluation.md",
                mime="text/markdown"
            )
            # Create a temporary file and use it
            with tempfile.NamedTemporaryFile(suffix=".docx") as temp:
                # Convert markdown to docx
                pypandoc.convert_text(result_md, 'docx', format='md', outputfile=temp.name)
                with open(temp.name, "rb") as f:
                    binary_docx = f.read()
                    st.download_button(
                        label="Download evaluation as docx file",
                        data=binary_docx,
                        file_name=f"{student_file_basename}_evaluation.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )


if __name__ == '__main__':
    main()
