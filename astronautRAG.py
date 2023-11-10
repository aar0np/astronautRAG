import os
import cassio
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import Cassandra
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

# define Astra DB vars
ASTRA_DB_ID = os.environ["ASTRA_DB_ID"]
ASTRA_DB_KEYSPACE = "vsearch"
ASTRA_DB_TOKEN = os.environ['ASTRA_DB_APPLICATION_TOKEN']
KEYSPACE_NAME = ASTRA_DB_KEYSPACE
TABLE_NAME = 'astronaut_openai_vectors'

# connect to Astra DB
cassio.init(
    token=ASTRA_DB_TOKEN,
    database_id=ASTRA_DB_ID,
    keyspace=KEYSPACE_NAME,
)

astronaut_template = """
You are a NASA historian, tasked with answering space enthusiasts' questions.
You must answer based only on the provided context, do not make up any fact.
Your answers must provide factual details.
You MUST refuse to answer questions on other topics than NASA astronaut history,
as well as questions whose answer is not found in the provided context.

CONTEXT:
{context}

QUESTION: {question}

YOUR ANSWER:"""

llm = ChatOpenAI()
embeddings = OpenAIEmbeddings() #1536

astronaut_prompt = ChatPromptTemplate.from_template(astronaut_template)
vectorstore = Cassandra(embedding=embeddings, table_name=TABLE_NAME, session=None, keyspace=None)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | astronaut_prompt
    | llm
    | StrOutputParser()
)

userInput = "which three astronauts flew on apollo 11?"

while userInput != "exit":
    print(chain.invoke(userInput))
    print("\n")
    userInput = input("Next question? ")

print("Exiting...")
