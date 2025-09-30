from langchain.llms import OpenAI

def run_langchain():
    llm = OpenAI(openai_api_key="your_api_key")
    print(llm("Hello from LangChain in Airflow!"))