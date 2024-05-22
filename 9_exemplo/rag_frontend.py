import streamlit as st
import rag_backend as demo

st.set_page_config(page_title= 'RAG')

if 'vector_index' not in st.session_state:
    with st.spinner("Wait for magic ..."):
        st.session_state.vector_index = demo.hr_index()

input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Submit", type="primary")

if go_button:

    with st.spinner("Tell me something"):
        response_content = demo.hr_rag_response(index=st.session_state.vector_index, question=input_text)
        st.write(response_content)