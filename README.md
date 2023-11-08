# astronautRAG and astronautLoader
Uses an OpenAI ChatGPT model to serve as a conversational knowledge base about NASA's astronaut history (data originally from Kaggle's [Astronaut database](https://www.kaggle.com/datasets/jessemostipak/astronaut-database?select=astronauts.csv)). While an OpenAI API key is required to access the model, the resulting vector embeddings are stored in DataStax Astra DB. Astra DB is accessed via an integration with [LangChain](https://python.langchain.com/docs/get_started/introduction) and [CassIO](https://cassio.org/).

## Requirements
 - A vector-enabled [Astra DB](https://astra.datastax.com) database
 - An Astra DB application token (with DBA priviliges)
 - An OpenAI account and API key
 - Environment variables defined for: `OPENAI_API_KEY`, `ASTRA_DB_APPLICATION_TOKEN`, and `ASTRA_DB_ID`:

```
export ASTRA_DB_APPLICATION_TOKEN=AstraCS:GgsdfsdQuMtglFHqKZw:SDGSDDSG6a36d8526BLAHBLAHBLAHc18d40
export ASTRA_DB_ID=cab0blah-blah-blah-blah-e4199blah536
export OPENAI_API_KEY=sk-6gblahblahblahbittyblahtpp
```

## Functionality

### astronautLoader
Loads data from the [astronauts.csv](astronauts.csv) file. The lines of the file are used to generate IDs (names of the astronauts). Both the names and the lines are then fed into the LangChain/CassIO/Cassandra integration with the `vectorstore.add_texts()` method.

### astronautRAG
Requres the **astronautLoader** program to be run first. It uses LangChain's chat prompt template (details of which can be seen in the code) to interact with the language model. It starts with the default question of "Which three astronauts flew on Apollo 11?"

Once it answers that question, it loops to ask for more questions until the command `exit` is entered.

## Output
```
» python astronautRAG.py
The three astronauts who flew on Apollo 11 were Michael Collins, Neil Armstrong, and Buzz Aldrin.
Next question? which astronauts attended the University of Minnesota?
Duane G. Carey attended the University of Minnesota-Minneapolis.
Next question? which astronauts attended Purdue University?
Eugene A. Cernan and Donald E. Williams attended Purdue University.
Next question? which astronauts flew on the Gemini 4 mission?
James A. McDivitt flew on the Gemini 4 mission.
Next question? What day was Jim Lovell born on?
Jim Lovell was born on March 25, 1928.
Next question? exit
Exiting...
```