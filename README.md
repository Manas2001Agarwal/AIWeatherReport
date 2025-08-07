# Problem Statement
In this project we have created an agentic weather expert chatbot that will answer questions related to weather condition etc. 

Example - 
1) What is the weather in New Delhi ?
2) What are types of Monsoon in India

To get real time answers of such questions we aim to build an RAG based Agentic Weather Chatbot that will answer queries. 

# Agent Workflow
We have created a REACT type agent with three tools. LLM acts as Brain. Based on the users query LLM decides whether to make a tool call and if yes which tool to call. 
Here we basically utlize three tools to answer user queries.
1) RAG pipeline - To refer to private (or proprietary) knowledge while giving answer to user queries.
2) OpenAIWeatherAPI: To get real time weather details of a place etc.

![REACT_Agent](https://github.com/user-attachments/assets/daf0055a-619c-4aaa-8f03-037cf0b83443)

# Component Used
1) Embedding LLM Model Used: Google-Gemini - "text-embedding-004"
2) Generative LLM Model Used: Groq - "openai/gpt-oss-120b"
3) Vector DB Used: QDrant Vector DB
   
# How to Launch the project
1) Clone the repo
   - git clone https://github.com/Manas2001Agarwal/agentic-trading-bot.git
   - cd agentic-trading-bot
2) Set Up Virtual Env
   - Use Conda : conda create --name agent_env python=3.10
   - conda activate agent_env
3) Install Dependencies
   - pip install -r requirements.txt
4) Set up .env file with below token
   - GROQ_API_KEY = 
   - GOOGLE_API_KEY = 
   - LANGSMITH_API_KEY = 
   - LANGSMITH_TRACING = 
   - LANGSMITH_ENDPOINT = 
   - LANGSMITH_PROJECT = 
   - OPENWEATHERMAP_API_KEY = 
   - QDRANT_API_KEY = 
5) Run main.py
   - uvicorn main:app --reload --port 8000
   - streamlit run streamli_ui.py

# Additional Info 
1) Created two endpoints using FastAPI
   - First to ingest the uploaded documents and load them into vector database. Or calling OpenAIWeatherAPI "\query" ==> That is basically Invoking langgraph workflow
   - Second to Agent (Graph) that will execute tools to get answers to question asked "\upload" ==> Invoking data ingestion pipeline
2) Created an Interactive UI components using Streamlit thay seeming integrated with both Fast API endpoints
3) Whether it is a .pdf or .docx we are accepting both file types and loading, chunking and storing them in Pinecone Vector DB

# Working Demo
https://www.loom.com/share/6927b3f19c324dab85b30143b31628c4?sid=fb76ed5c-38a4-4e9a-8909-78ae39158c48