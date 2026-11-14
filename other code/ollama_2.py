from langchain_ollama import OllamaLLM, ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# template = """
# Question: {question}

# 請使用中文回答此問題，以下是先前的對話紀錄:{history}
# """
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
  # elif user_input.lower() == "history":
  #   print(context)
  else:
    print("AI: ")
    for chunk in chain.stream({"question":user_input}):
    # for chunk in chain.stream({"question":user_input, "history":context}):
      print(chunk.content, end="", flush=True)
      response += chunk.content
    print("")
    # context += f"\nUser:{user_input}\nAI:{responce}"
      