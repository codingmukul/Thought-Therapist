from dotenv import load_dotenv
load_dotenv()
import os

# Load environment variables
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from langchain_community.graphs import Neo4jGraph
graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

from langchain_groq import ChatGroq
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")

from langchain.chains import GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, exclude_types=["Genre"], verbose=True)

examples = [
    {
        "question": "Give the Introduction/Career Objection of Mukul?",
        "query": "MATCH (a:Person)-[:HAS_CAREER_OBJECTIVE]->(n) RETURN n.Description",
    },
    {
        "question": "Tell me about Mukul!",
        "query": "MATCH (a:Person)-[:INTRODUCES]->(n) RETURN n.Description",
    },
    {
        "question": "Tell me about education.",
        "query": "MATCH (a:Person )-[:HAS_EDUCATION]->(n) RETURN n.institution, n.year, n.education_level, n.SCORE, n.Percentage",
    },
    {
        "question": "What is CGPA of Mukul in Class X",
        "query": "MATCH (a:Person)-[:HAS_EDUCATION]->(n:Education) WHERE n.education_level = 'Class X' RETURN n.SCORE",
    },
    {
        "question": "Tell me about Achievements of Mukul.",
        "query": "MATCH (a:Person)-[:HAS_ACHIEVED]->(n) RETURN n.Score, n.year, n.name, n.Rank",
    },
    {
        "question": "Tell me about work experience of Mukul.",
        "query": "MATCH (a:Person )-[:HAS_EXPERIENCE]->(n) RETURN n.domain, n.company, n.position, n.start_year, n.end_year",
    },
    {
        "question": "What project did Mukul make? and what are skills used in those?",
        "query": "MATCH (a:Person)-[:WORKED_ON]->(n) MATCH (n)-[:USING]->(q) RETURN n.description, q.name",
    },
    {
        "question": "What are your skills?",
        "query": "MATCH (a:Person)-[:HAS_SKILL]->(n) RETURN n.name",
    },
    {
        "question": "What are your weaknesses?",
        "query": "MATCH (a:Person)-[:WEAKNESS]->(n) RETURN n.description",
    },
    {
        "question": "What are your strengths?",
        "query": "MATCH (a:Person)-[:HAS_STRENGTH]->(n) RETURN n.description",
    },
    {
        "question":"What are the langauges you know?",
        "query": "MATCH (a:Person)-[:KNOWS_LANGUAGE]->(n) RETURN n.name, n.speaking, n.writing",

    }
]

from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

# Create the example prompt template
example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

# Create the few-shot prompt template
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="You are a Neo4j expert. This database is a CV of a guy named Mukul. Strictly remember, the only Person here is Mukul Aggarwal and he is often referred as developer, you and mukul. Given an input question, create a syntactically very accurate Cypher query.",
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question"]
)

# Create the GraphCypherQAChain with the custom prompt
chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, cypher_prompt=prompt, verbose=True)

import streamlit as st

user_prompt = st.chat_input("Ask a question about Me")

if user_prompt:
    try:
        result = chain.invoke(user_prompt)
        st.write(result['result'])
    except Exception as e:
        st.write("Please try again!")

