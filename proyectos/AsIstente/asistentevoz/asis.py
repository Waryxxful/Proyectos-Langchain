from streamlit_mic_recorder import speech_to_text
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import AIMessage, HumanMessage
from langchain_core.callbacks import StdOutCallbackHandler

load_dotenv()

# Creación del prompt de la conversación
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Eres un asistente que ayuda a organizar la vida de las personas."
        " Además de agendar el evento {evento}, debes sugerir horarios adecuados"
        " para preparaciones previas, asegurando que no se superpongan con otras actividades."
        " También recordarás actividades pendientes. Proporciona respuestas claras y organizadas."
    ),
    HumanMessagePromptTemplate.from_template("{input}")
])

# Creación del modelo de lenguaje y la memoria
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
memory = ConversationBufferWindowMemory(k=2, return_messages=True)

# Función para guardar y cargar conversaciones
def save_conversation(conversation, filename="conversation.txt"):
    try:
        with open(filename, "w") as f:
            for message in conversation:
                f.write(f"{message['sender']}: {message['content']}\n")
    except Exception as e:
        print("Error guardando la conversación:", e)

def load_conversation(filename="conversation.txt"):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Función de conversación con el asistente
def conversacion(input_text):
    messages = [
        HumanMessage(content=input_text),
        AIMessage(content=load_conversation())
    ]
    response = llm.invoke(messages)
    
    save_conversation([{"sender": "Usuario", "content": input_text}, 
                       {"sender": "Asistente", "content": response.content}])
    
    return response.content

# Creación de la interfaz en Streamlit
st.title("Asistente de voz")
st.write("Hable al micrófono para comenzar")

text = speech_to_text(language='es', use_container_width=True, just_once=False, key='STT')

if text:
    st.write("Usted dijo: ", text)
    response = conversacion(text)
    st.write("Respuesta: ", response)
