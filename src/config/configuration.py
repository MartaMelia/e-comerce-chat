import box
import yaml
import os
import requests
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings



with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def configure():
    _init_data()
    _init_vector()


def _init_data():
    directory = os.path.dirname(cfg.DATA_SAVE_PATH)
    print(directory)

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, cfg.DATA_FILE_NAME)

    if os.path.exists(file_path):
        print("Data has already initialized.")
        return

    print("Downloading data...")
    response = requests.get(cfg.DATA_LINK, allow_redirects=True)

    with open(file_path, 'wb') as file:
        file.write(response.content)

    print("Data saved succesfully")


def _init_vector():
    vector_path = os.path.join(cfg.VECTOR_SAVE_PATH, cfg.VECTOR_FILE_NAME)

    if os.path.exists(vector_path):
        print("vector has already initialized.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model=cfg.MODEL_EMBEDDING, google_api_key=cfg.GOOGLE_API_KEY)
    file_path = os.path.join(cfg.DATA_SAVE_PATH, cfg.DATA_FILE_NAME)

    print("Loading data file.")
    loader = CSVLoader(file_path, encoding="utf-8")
    documents = loader.load()


    print("Saving as a vector file")
    Chroma.from_documents(documents, embeddings, persist_directory=vector_path)

    print("Vector file saved successfully")
