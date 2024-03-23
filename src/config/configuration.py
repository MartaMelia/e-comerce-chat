import box
import yaml
import os
import requests
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pandas as pd



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

    _data_filter()


def _data_filter():
    directory = os.path.dirname(cfg.DATA_SAVE_PATH)
    file_path = os.path.join(directory, cfg.DATA_FILE_NAME)

    df = pd.read_csv(file_path)
    
    df = df.dropna(axis=1, how='all')
    df.drop(columns=['Is Amazon Seller', 'Upc Ean Code', 'Variants'], inplace=True)

    links_split = df['Image'].str.split('|', expand=True)

    links_split = links_split.iloc[:, :3]

    new_column_names = [f'Image_{i+1}' for i in range(links_split.shape[1])]
    links_split.columns = new_column_names

    df = pd.concat([df, links_split], axis=1)

    df.drop('Image', axis=1, inplace=True)

    df.to_csv(file_path, index=False)


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
