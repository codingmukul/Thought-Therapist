Hi Everyone, 

This is my new project based on Gen AI, named as Thought Therapist.

It is a streamlit website, which has three sections:

1. Thought Therapist
2. FAQ (Frequently Asked Questions)
3. Know more about developer.

**Thought Therapist**

It is a chatbot, which chats with a person facing mental health issues. It is a *fine-tuned* model on LAMINI, which is then customly integrated with *Langchain* and streamlit to create the working web page. It is based on LLM Meta-Llama-3.1-8B. It has the feature of keeping the context of chat history in order to provide valuable feedback.

**FAQ**

It is a question-answering prompt, which answer frequenty asked questions based on mental health based on a CSV file containing the FAQ's. It used *Vector Data Base* to store the vector embeddings and it used *Retrieval-Augmented Generation(RAG)* in order to produce output from the given prompt and the context. It used *EDEN AI* for embeddings and *GROQ AI* as LLM provider.

**Know more about developer**

It is a question-answering prompt, which answer any queries about the developer. Here, I have used *Graph Data Base* by using *neo4j*. I have made a graph Data base about me and then I have integrated this database with Langchain to answer the queries based on the information in database. Here, you can ask questions like

1. "What is your name? "

2. "Tell me about your experience?"

3. "Which Languages do you know?"

4. "Give me a introduction of yourself."

## Files and Folders details

1. **.streamlit**: It is a folder that contains pages information on streamlit i.e. details and structure of three pages.

2. **FAQ.CSV**: It contains the frequently asked questions in CSV format.

3. **FAQ_Vector_DB.py** : It contains a python program, which was used to create the vector embeddings for the **FAQ.csv** and store them in a database i.e. **FAQ_db**.

4. **FAQ_db** : Database for embeddings.

5. **Model_Fine-tuning**: It contains a python program which fine tunes the model on LAMINI based on data provided.

6. **Therapist.py**: The first section of the website.

7. **FAQ.py**: The second section of the website.

8. **about.py**: The third section of the website.

9. **app.py** L The website starts from this python file.

10. **GraphDB_Mukul**: Contains the structure of database created for section *Know more about developer*. (Just for reference, this image isn't used anywhere.)

Please find the demo at: <a>https://drive.google.com/file/d/1H8CtNSd8t5JhvqaDO73i4LuchCwAWKEG/view?usp=drive_link<a>