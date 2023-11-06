import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.vectorstores import Cassandra
from langchain.embeddings  import HuggingFaceEmbeddings

# define Astra DB vars
ASTRA_CLIENT_ID = 'token'
ASTRA_DB_KEYSPACE = "vsearch"
ASTRA_DB_TOKEN = os.environ['ASTRA_DB_APPLICATION_TOKEN']
KEYSPACE_NAME = ASTRA_DB_KEYSPACE
SECURE_CONNECT_BUNDLE_PATH = os.environ['ASTRA_SCB_PATH']
TABLE_NAME = 'astronaut_vectors'

# connect to Astra DB
cloud_config= {
    'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider(ASTRA_CLIENT_ID, ASTRA_DB_TOKEN)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider, protocol_version=4)
session = cluster.connect()

embeddings = HuggingFaceEmbeddings()
vectorstore = Cassandra(embeddings, session, KEYSPACE_NAME, TABLE_NAME)

# load and process file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

src_file_name = os.path.join(BASE_DIR, "astronauts.csv")
lines = [
    line.strip()
    for line in open(src_file_name).readlines()
    if line.strip()
    if line[0] != "name"
]

# ID == name to prevent duplicates on multiple runs
names = [
	line.split(",")[0]
	for line in lines
	if line.split(",")[0] != "name"
]

for line in lines:
	print(line)

#vectorstore.add_texts(texts=lines, ids=names)

#ids = ["_".join(line.split(" ")[:2]).lower().replace(",", " ") for line in lines]

for id in names:
	print(id)

#vector_store.add_texts(texts=lines, ids=ids)
