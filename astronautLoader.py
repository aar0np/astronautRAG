import os
import cassio
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.vectorstores import Cassandra
#from langchain.chat_models import ChatOpenAI
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

# init LLM and embeddings model
embeddings = OpenAIEmbeddings() #1536
vectorstore = Cassandra(embedding=embeddings, table_name=TABLE_NAME, session=None, keyspace=None)

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
