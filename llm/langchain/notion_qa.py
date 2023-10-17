from getpass import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass("OpenAI API Key:")
NOTION_TOKEN = getpass("notion_token:")
DATABASE_ID = getpass("db_id:")

from langchain.document_loaders import NotionDBLoader

loader = NotionDBLoader(
    integration_token=NOTION_TOKEN,
    database_id=DATABASE_ID,
    request_timeout_sec=30,  # optional, defaults to 10
)

raw_docs = loader.load()
print(len(raw_docs))

# Uncomment the following line if you need to initialize FAISS with no AVX2 optimization
# os.environ['FAISS_NO_AVX2'] = '1'
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


embeddings = OpenAIEmbeddings()
# db = FAISS.from_documents(raw_docs, embeddings)
import time
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=50, separator="\n")
splitted_documents = text_splitter.split_documents(raw_docs[5])
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQAWithSourcesChain
db=None
llm = ChatOpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'], max_tokens=500, model_name="gpt-3.5-turbo")
for document in splitted_documents:
        if db is None:
            db = FAISS.from_documents([document], embeddings)
            chain = ConversationalRetrievalChain.from_llm(llm, db.as_retriever())
            chat_history = []
        else:
            db.add_documents([document])
        time.sleep(60)  # wait for 60 seconds before processing the next document
query = ""
docs = db.similarity_search(query)
print(docs[0].page_content)


chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, retriever=db.as_retriever())
result = chain({"question": query})
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")

