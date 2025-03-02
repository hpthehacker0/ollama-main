from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import Chatollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
model_local = Chatollama (model="mistral")
# 1. Split data into chunks
urls = [
"https://ollama.com/",
"https://ollama.com/blog/windows-preview",
"https://ollama.com/blog/openai-compatibility",
]
docs = [WebBaseLoader(url). load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500,
chunk_overlap = 100)
doc_splits = text_splitter.split_documents(docs_list)
# 2. Convert documents to Embeddings and store them
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embeddings.ollama.ollamaEmbeddings (model='nomic-embed-text'),
)
retriever = vectorstore.as_retriever()
# 3. Before RAG
print("Before RAG\n")
before_rag_template = "What is {topic}"
before_rag_prompt = ChatPromptTemplate.from_template(before_rag_template)
before_rag_chain = before_rag_prompt | model_local | StrOutputParser ()
print (before_rag_chain. invoke({"topic": "ollama"}))
