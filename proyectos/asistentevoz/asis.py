from streamlit_mic_recorder import speech_to_text
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
from langchain_community.llms import ollama
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate,ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools, create_react_agent
from langchain.memory import ConversationBufferMemory
load_dotenv()

#creacion de los modelos de lenguaje y el agente
llm =  ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_react_agent()

#creador de archivo de texto con la conversacion 
def save_conversation(conversation, filename="conversation.txt"):
    with open(filename, "w") as f:
        for message in conversation:
            f.write(f"{message['sender']}: {message['content']}\n")
def load_conversation(filename="conversation.txt"):
    with open (filename, "r") as f:
        conversation = f.read() 
    return conversation
#prompt de carga de contexto y funcion de carga de contexto y funcionmiento del agente
def carga_contexto(agent,filename):
    context = load_conversation(filename)
    prompt = "la conversacion hasta ahora es {conext}"
    prompt_template = ChatPromptTemplate.from_template(prompt)
    agent.run(prompt_template,context=context)    
    return True

carga_contexto(agent,"conversation.txt")
if carga_contexto(agent,"conversation.txt"):
    st.write("Carga de contexto exitosa")



#creacion de la pagina y la utilizacion del agente 
st.title("Asistente de voz")
st.write("Hable al micrófono para comenzar")

text = speech_to_text(language='es', use_container_width=True,just_once=False,key='STT')


if text:
    st.write("Usted dijo: ", text)
    response = agent.run(text)
    save_conversation(response.content)
    st.write("Respuesta: ", response.content)
