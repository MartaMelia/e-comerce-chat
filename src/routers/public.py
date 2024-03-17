from fastapi import APIRouter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from .request import AssistantRequest
from langchain.vectorstores import Chroma
import box
import yaml
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from .prompts import assistant_prompt


router = APIRouter()

with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


@router.post("/assistant")
async def assistant(request: AssistantRequest):
    vector_path = os.path.join(cfg.VECTOR_SAVE_PATH, cfg.VECTOR_FILE_NAME)

    embeddings = GoogleGenerativeAIEmbeddings(model=cfg.MODEL_EMBEDDING, google_api_key=cfg.GOOGLE_API_KEY)

    db = Chroma(persist_directory=vector_path, embedding_function=embeddings)

    retriever = db.as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT})

    llm = ChatGoogleGenerativeAI(model=cfg.MODEL, google_api_key=cfg.GOOGLE_API_KEY)

    prompt = PromptTemplate.from_template(assistant_prompt)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    response=retrieval_chain.invoke({"input": request.question})

    return {"answer": response["answer"]}
