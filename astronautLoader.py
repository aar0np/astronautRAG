import os
from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

# define Astra DB vars
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')
ASTRA_DB_KEYSPACE = "vsearch"
TABLE_NAME = 'astronaut_huggingface_vectors'

# init LLM and embeddings model
#embeddings = OpenAIEmbeddings() #1536
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False},
)

# connect to Astra DB
vectorstore = AstraDBVectorStore(
    embedding=embeddings,
    collection_name=TABLE_NAME,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_TOKEN,
    namespace=ASTRA_DB_KEYSPACE,
)

# load and process file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

src_file_name = os.path.join(BASE_DIR, "astronauts.csv")
lines = [
    line.strip()
    for line in open(src_file_name).readlines()
    if line.split(",")[0] != "name"
]

# ID == name to prevent duplicates on multiple runs
names = [
	line.split(",")[0]
	for line in lines
	if line.split(",")[0] != "name"
]

vectorstore.add_texts(texts=lines, ids=names)
