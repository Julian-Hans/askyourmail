# ASKYOURMAIL
A conversational interface for retrieving emails and answering natural language queries based on them.

## TODOS:
### Extract emails from an imap server:
We need a way to expose emails to our system. Implement an *email* class in python (or use the imap tools one) that contains the most important metadata for our search. This includes: subject, sender, recipient, content, date received etc. Optimally, we would be able to build a *conversation* class from these, which we will use to populate our database for the retrieval system. 

For our MVP, we can start by just loading a dataset (TODO: find one on keggle) and compiling it into *emails* and *conversations*, making it accessible in python.

Later down the line, we could connect to an imap server to export (and update) our mails from there.
Potential library to achieve this: 
- https://pypi.org/project/imap-tools/


### Insert extracted emails into vector store
Our most basic retrieval approach will be a simple vector store like: 
- https://www.trychroma.com
- https://www.pinecone.io

We will create chunks of our *emails* or *conversations*, tokenize and generate embeddings (most likely through openAI) for them and insert these into our DB. For more complex knowledge modeling, we could use a graph-database like:
- http://neo4j.com

but for the MVP a simple rag retrieval should be enough.

### Build a Self-Rag Graph
In order to have our llm of choice (openAI) generate answers grounded on the base truth of our Email data, we will implement a self-rag Graph (the basic outlines should already be in MainGraph.py), similar to this example:
- https://www.youtube.com/watch?v=sgnrL7yo1TE


### Come up with an evaluation system
We need to measure the performance of our system. Since we will be asking natural language queries, we have to come up with a validation dataset that test if the response (returned *email* / *conversation*) is correct for our query. Ideas: evaluate similar to ndcg@10, hit@10 etc, use metrics presented in lecture. 

### Develop rudimentary frontend
To make our MVP interactive, we should develop a frontend. It should feature a conversational interface (like chatgpt), where one can enter a query, as well as read the response. Since our response will be grounded in our data, we need a way to output the sources of the generated answer and present them (or their IDs) to the user.
Potential libraries to achieve this: 
- https://streamlit.io
- https://www.gradio.app