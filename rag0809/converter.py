from langchain_community.document_loaders import PyMuPDFLoader
# from llama_index.readers.file import PyMuPDFReader
import os

for file in os.listdir("rawPDF"):
    loader = PyMuPDFLoader(f"rawPDF/{file}")
    data = loader.load()
    # loader = PyMuPDFReader()
    # documents = loader.load(file_path=f"rawPDF/{file}")
    temp = ""
    for i in data:
        temp += i.page_content
    with open(f"input/{file[:10]}.txt", "w") as f:
        f.write(temp)
# loader = PyMuPDFReader()
# documents = loader.load(file_path="rawPDF/SILK Nature Reviews Neurology 2019.pdf")