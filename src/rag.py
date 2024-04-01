from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import bedrock as llm
from langchain_community.embeddings import bedrock as embeddings
from langchain_community.vectorstores import faiss
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from typing import List
from invoice import Invoice
import boto3


class RAG():

    def __init__(self, mistral_api_key) -> None:
        self.__bedrock_client = boto3.client(
            service_name='bedrock-runtime', region_name='us-east-1')

        self.__llm = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-large-latest")

        self.__bedrock_embeddings = embeddings.BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1", client=self.__bedrock_client)

        self.__prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert at identifying invoice data in text. "
                    "Only extract data related to the invoice. Extract nothing if no important information can be found in the text.",
                ),
                # MessagesPlaceholder('examples'), # Keep on reading through this use case to see how to use examples to improve performance
                ("human", "{text}"),
            ]
        )

    def text_splitter(self, document_text: str) -> List[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        return text_splitter.split_text(document_text)

    def vector_store(self, text_chunks):

        self.__vectorstore = faiss.FAISS.from_texts(
            texts=text_chunks, embedding=self.__bedrock_embeddings)

        return self.__vectorstore

    def __setExtractor(self):
        extractor = self.__prompt | self.__llm.with_structured_output(
            schema=Invoice)

        return extractor

    def get_response(self, query: str, vectorstore: faiss.FAISS):
        retriever = vectorstore.as_retriever()

        rag_extractor = {
            "text": retriever
        } | self.__setExtractor()

        return rag_extractor.invoke(query)
