from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.tools import get_company_information

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)

llm_with_tools = llm.bind_tools(
    [get_company_information]
)

response = llm_with_tools.invoke(
    """
    I need information about Acme Manufacturing.

    Use the available company information tool to find
    information about this company.
    """
)

print(response)