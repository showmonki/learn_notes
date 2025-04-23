from llama_index.core.base.embeddings.base import similarity
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent, ReActAgent
from llama_index.core.tools import FunctionTool, QueryEngineTool


# login()


def reverse_str(s:str) -> str:
    """ return reversed string"""
    return  s[::-1]

def upper_str(s:str) -> str:
    """ return reversed string"""
    return  s.upper()

def lower_str(s:str) -> str:
    """ return reversed string"""
    return  s.lower()

# model_url = '../peftLoraFunctionCalling/google/gemma-2-2b-it'
# # model_url = 'Qwen/Qwen2.5-Coder-32B-Instruct'
# llm = HuggingFaceInferenceAPI(model_name=model_url,token=token)
from llama_index.llms.ollama import Ollama
llm = Ollama(model="qwen2.5:7b-instruct", request_timeout=120.0)
agent = AgentWorkflow.from_tools_or_functions(
    tools_or_functions=[FunctionTool.from_defaults(reverse_str)],
    llm=llm,
    system_prompt='You are an agent that can handling with str using provided tools.'
)

async def agent_run(query):
    resp = await agent.run(query)
    return resp
# response = await agent.run('what is the reversed result for "algorithm"')
# response = agent_run('what is the reversed result for "algorithm"')

from llama_index.core.workflow import Context
ctx = Context(agent)
response = agent_run("i need to build a rag", ctx=ctx)
response = agent_run("what should i to do", ctx=ctx)

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
db = chromadb.PersistentClient(path='./ollamembed')
chroma_collection = db.get_or_create_collection('learn')
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.embeddings.ollama import OllamaEmbedding
embed_model = OllamaEmbedding(
    model_name="bge-m3",
    # base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

# embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')
index=VectorStoreIndex.from_vector_store(vector_store,embed_model=embed_model)

query_engine = index.as_query_engine(llm=llm, similarity_top_k=3)
query_engine_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name='query_search',
    description='search information about llamaindex',
    return_direct=False,
)

query_engine_agent = AgentWorkflow.from_tools_or_functions(
    tools_or_functions=[query_engine_tool],
    llm=llm,
    system_prompt="You are a helpful assistant that has access to a database containing information about llamaindex."
)
handle=query_engine_agent.run('what is the llamaindex')
str_agent = ReActAgent(
    name='str_manipulate',
    description='performs basic string operations',
    system_prompt='You are a string manipulate assistant. use tools for any string operation.',
    tools = [reverse_str, lower_str,upper_str],
    llm=llm,
)
query_agent = ReActAgent(
    name='search_db',
    description='looks up information about llamaindex',
    system_prompt='',
    tools=[query_engine_tool],
    llm=llm,
)
agent = AgentWorkflow(agents=[str_agent,query_agent],root_agent='str_manipulate')
handler=agent.run(user_msg="convert 'abc' to upper string")
# resp = await handler