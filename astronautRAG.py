import os
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub

# define Astra DB vars
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')
ASTRA_DB_KEYSPACE = "vsearch"
TABLE_NAME = 'astronaut_huggingface_vectors'

astronaut_template = """
You are a NASA historian, tasked with answering questions from space enthusiasts.
You must answer based only on the provided context, do not make up any fact.
Your answers must provide factual details.
You MUST refuse to answer questions on other topics than NASA astronaut history,
as well as questions whose answer is not found in the provided context.

CONTEXT:
{context}

QUESTION: {question}

YOUR ANSWER:"""
#llm = ChatOpenAI()
llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    model_kwargs={
        "max_new_tokens": 512,
        "top_k": 30,
        "temperature": 0.01,
        "repetition_penalty": 1.03,
    },
)
# init LLM and embeddings model
#embeddings = OpenAIEmbeddings() #1536
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False},
)

astronaut_prompt = ChatPromptTemplate.from_template(astronaut_template)
vectorstore = AstraDBVectorStore(
    embedding=embeddings,
    collection_name=TABLE_NAME,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_TOKEN,
    namespace=ASTRA_DB_KEYSPACE,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | astronaut_prompt
    | llm
    | StrOutputParser()
)

userInput = "which three astronauts flew on Apollo 11?"

while userInput != "exit":
    print(chain.invoke(userInput))
    print("\n")
    userInput = input("Next question? ")

print("Exiting...")
