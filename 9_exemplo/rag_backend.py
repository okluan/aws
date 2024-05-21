import os
from langchain_community.document_loaders import PyPDFLoader

data_load = PyPDFLoader('https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf')
data_test = data_load.load_and_split()
print(len(data_test))
