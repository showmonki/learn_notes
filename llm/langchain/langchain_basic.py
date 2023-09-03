from langchain.tools import BaseTool
from math import pi
from typing import Union
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent

from typing import List, Optional, Mapping, Any
from functools import partial

from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from transformers import AutoModel, AutoTokenizer

class CircumferenceTool(BaseTool):
    name = "Circumference calculator"
    description = "use this tool when you need to calculate a circumference using the radius of a circle"

    def _run(self, radius: Union[int, float]):
        return radius

# initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
llm = ChatOpenAI(
        openai_api_key="",
        temperature=0,
        model_name='gpt-3.5-turbo'
)



# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
)


tools = [CircumferenceTool()]

# initialize agent with tools
agent = initialize_agent(
    agent='zero-shot-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=conversational_memory,
    handle_parsing_errors=True
)

agent("Use tool to calculate the circumference of a circle that has a radius of 2mm")
