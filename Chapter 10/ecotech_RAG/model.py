from dotenv import load_dotenv
load_dotenv()

from langchain_cohere import ChatCohere
from langchain_core.output_parsers import StrOutputParser
from prompting import chat_prompt_template

model = ChatCohere(model="command-r-plus-08-2024")

chain = (
    chat_prompt_template | model | StrOutputParser()
)



