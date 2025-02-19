import streamlit as st
from langchain_experimental.tools import PythonREPLTool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor 
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
def save_history(question, answer):
    with open('history.txt', 'a') as f:
        f.write(f'{datetime.datetime.now()}: Pregunta: {question} -> Respuesta: {answer}\n\n')
def load_history():
    with open('history.txt', 'r') as f:
        return f.read()
def clear_history():
    if os.path.exists('history.txt'):
        os.remove('history.txt')

def pregunta(pregunta):
    respuesta = agent_executor.invoke(f"¿Qué código de Python corresponde a la pregunta: {pregunta}?")
    return respuesta

tools = [PythonREPLTool()]
base_prompt = hub.pull("hwchase17/react")
prompt = base_prompt.partial(instructions="Eres una IA que responde preguntas en lenguaje natural y entregas el codigo python correspondiente a lo que se te pide no entregas la respuesta solo el codigo")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature= 0)
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)

st.title('Asistente de lenguaje natural para python')
st.write('Este asistente puede responder preguntas sobre codigo python.')

pregunta = st.text_input('Escribe tu pregunta:')
if st.button('preguntar'):
    respuesta = agent_executor.invoke({"input": pregunta})
    st.write(respuesta)

