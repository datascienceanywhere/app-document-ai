from langchain_openai import ChatOpenAI


def extraction_model(model: str="gpt-5-mini", temperature: float=0.7):
    llm = ChatOpenAI(model=model, temperature=temperature)

    return llm
    