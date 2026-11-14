import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "ai_project_2024"

from langchain_ollama import OllamaLLM, ChatOllama
from langchain_core.prompts import ChatPromptTemplate

template = """{question}"""
model = ChatOllama(model="test")
prompt = ChatPromptTemplate.from_template(template=template)

chain = prompt | model
context = ""
while True:
  response = ""
  user_input = input("You: ")
  if user_input.lower() == "exit":
    break
  else:
    print("AI: ")
    for chunk in chain.stream({"question":user_input}):
      print(chunk.content, end="", flush=True)
      response += chunk.content
    print("")