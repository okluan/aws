import os
import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import BedrockEmbeddings
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain_community.vectorstores import FAISS
from langchain.llms.bedrock import Bedrock
from dotenv import load_dotenv
load_dotenv()

boto3.setup_default_session(
    aws_access_key_id = os.getenv("aws_access_key_id"),
    aws_secret_access_key= os.getenv("aws_secret_access_key"),
    region_name = os.getenv("region_name"))

def hr_index():               
    data_load = PyPDFLoader('https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf')

    data_split = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size = 200)

    data_embedding = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1')

    data_index = VectorstoreIndexCreator(
        text_splitter=data_split,
        embedding= data_embedding,
        vectorstore_cls= FAISS
    )

    db_index = data_index.from_loaders([data_load])

    return db_index

def hr_llm():
    llm = Bedrock(
        model_id= 'anthropic.claude-v2',
        model_kwargs={
            "max_tokens_to_sample": 300,
                "temperature": 0.1,
                "top_p":0.9
        }
    )
    return llm

def hr_rag_response(index, question):
    rag_llm = hr_llm()
    hr_rag_query = index.query(question=question, llm=rag_llm)
    return hr_rag_query



