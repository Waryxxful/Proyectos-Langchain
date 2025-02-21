import streamlit as st
from langchain_openai import ChatOpenAI ,OpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from fpdf import FPDF
from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import load_tools , initialize_agent, AgentType
load_dotenv()
search = GoogleSerperAPIWrapper()
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature= 0.5)
template_agent  = '''
Busca en Google recetas con los ingredientes proporcionados. Devuelve una lista con almenos 3 recetas con su preparación y tiempo estimado. todo en español siempre.

el formato de la repuesta debe ser el siguiente: 
titulo de la receta:
ingredientes:
preparación:
tiempo estimado:
'''

template_llm = '''
debes inventar un titulo para el  archivo pdf que se generará con las recetas encontradas.{recetas}
'''

prompt = PromptTemplate.from_template(template_llm)

chain = LLMChain(llm=llm, prompt=prompt)

tools= [
    Tool(
        name='Intermediate Answer', func= search.run,description=template_agent
    )
]


agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,handle_parsing_errors=True,k = 5
)


def pregunta(ingredientes):
    respuesta = agent.run(f"Busca recetas con los ingredientes: {ingredientes}")

    return respuesta

def titulo(recetas):
    respuesta = chain.invoke(f"debes inventar un titulo para el  archivo pdf que se generará con las recetas encontradas. todo en español{recetas}")
    return respuesta


st.title('Recetario')
st.write('Este asistente puede buscar recetas con los ingredientes que tu le entregues.')
ingredientes = st.text_input('Escribe los ingredientes que tienes separados por comas:')
if st.button('Buscar recetas'):
    respuesta = pregunta(ingredientes)
    st.write(respuesta)
    titulo_pdf = titulo(respuesta)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = respuesta, ln = True, align = 'C')
    pdf.output(titulo_pdf['text']+'.pdf')
    st.write('Se ha generado un pdf con las recetas encontradas')
