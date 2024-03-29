from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import bedrock as llm
from langchain_community.embeddings import bedrock as embeddings
from langchain_community.vectorstores import chroma
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from typing import List
import boto3


template = """Use the following pieces of context to extract the asked data at the end and make sure you output it in a json format. Don't say anything else but the asked data.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.

{context}

Question: {question}

Helpful Answer:"""


class RAG():

    def __init__(self) -> None:
        self.__bedrock_client = boto3.client(
            service_name='bedrock-runtime', region_name='us-east-1')

        self.__llm = llm.Bedrock(client=self.__bedrock_client,
                               model_id="cohere.command-text-v14")

        self.__bedrock_embeddings = embeddings.BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1", client=self.__bedrock_client)

        self.__prompt = PromptTemplate.from_template(template)

    def text_splitter(self, document_text: str) -> List[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        return text_splitter.split_text(document_text)

    def vector_store(self, text_chunks):

        self.__vectorstore = chroma.Chroma.from_texts(
            texts=text_chunks, embedding=self.__bedrock_embeddings)

        return self.__vectorstore

    def get_response(self, query: str, vectorstore: chroma.Chroma):
        retriever = vectorstore.as_retriever()

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | self.__prompt
            | self.__llm
            | JsonOutputParser()
        )

        return rag_chain.invoke(query)
