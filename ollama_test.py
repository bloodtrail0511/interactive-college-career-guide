from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3.1")
conversation = ConversationChain(llm=llm)
print(conversation.prompt.template)

from langchain.chains.conversation.memory import ConversationBufferMemory

conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)
conversation_buf("Good morning AI!")
conversation_buf("How are you?")
conversation_buf("What's the weather today?")