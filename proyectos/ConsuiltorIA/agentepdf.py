#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate,ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import SimpleSequentialChain, LLMChain,TransformChain
from dotenv import load_dotenv
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.agents import load_tools,initialize_agent,AgentType,create_react_agent,AgentExecutor
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_core.prompts import PromptTemplate
import streamlit as st
import os

# #### Creacion del modelo 

# In[4]:


load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature= 0.2)
embedings = OpenAIEmbeddings()


# #### Vectorizacion del pdf ####
# 
#  

# In[5]:

def vectorizacion_pdf(pdf):
    # Guardar el archivo temporalmente
    temp_path = os.path.join(".", pdf.name)  # Guarda el archivo en el directorio actual
    with open(temp_path, "wb") as f:
        f.write(pdf.getbuffer())

    try:
        # Ahora pasamos la ruta del archivo a PDFPlumberLoader
        loader = PDFPlumberLoader(temp_path)
        docs = loader.load()
        text = "\n".join([page.page_content for page in docs])

        pdf_splitter = CharacterTextSplitter(chunk_size=900, chunk_overlap=80)
        texts = pdf_splitter.split_text(text)
        
        # Agregar metadatos vacíos para evitar el error
        documents = [Document(page_content=t, metadata={"source": pdf.name}) for t in texts]

        persist_path = f"./{pdf.name}_bd"  # Ruta donde se guardará la BD vectorizada

        vector_store = SKLearnVectorStore.from_documents(
            documents=documents,
            embedding=embedings,
            persist_path=persist_path,
            serializer="parquet",
        )

        return vector_store.persist()
    
    finally:
        os.remove(temp_path)  # Eliminar el archivo temporal después de usarlo

# #### Consulta sobre el pdf ####

# In[6]:


def consulta_pdf(vector_store,consulta):
    #Cargamos la BBDD de vectores
    vector_store_connection = SKLearnVectorStore(
    embedding=embedings, persist_path=vector_store, serializer="parquet"
)
    print("Una instancia de la BBDD de vectores se ha cargado desde ", vector_store)
    #Realizamos la consulta a la BBDD de vectores
    docs = vector_store_connection.similarity_search(consulta, k = 2)
    return docs


# #### consulta sobre el extracto de pdf ####

# In[31]:


prompt_template = PromptTemplate.from_template(
    "Eres un agente que responde preguntas {input} sobre un extracto de PDF {extracto}"
)


# In[33]:


qa_chain = LLMChain(llm=llm, prompt=prompt_template)


# #### FRONT

# In[ ]:


st.title("Consulta de documentos PDF")
st.write("Este programa permite realizar consultas en documentos PDF...solo pdf por ahora")
pdf = st.file_uploader("Sube tu archivo PDF")
if pdf:
    st.write("Archivo subido correctamente")
    st.write(pdf)
    ruta= pdf.name + "_bd"  
    st.write(ruta)
    if st.button("Vectorizar"):
        vector_store = vectorizacion_pdf(pdf)
        st.write("Archivo vectorizado correctamente")
    consulta = st.text_input("Ingrese su consulta")
    if st.button("Consultar"):
        docs = consulta_pdf(ruta,consulta)
        if docs:
            st.write("Consulta realizada correctamente")
            st.write(docs[0].page_content)
            
            response = qa_chain.run({"input": consulta, "extracto": docs[0].page_content})
            st.write('la ia responder ' +  response)
        else:
            st.write("Error en la consulta")
else:
    st.write("No se ha subido ningun archivo")



