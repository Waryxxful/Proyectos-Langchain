Este es un proyecto en alpha el cual consta de una aplicacion  IA con la libreria langchain para procesar y hacer  consultas sobre un PDF, actualmente solo soporta documentos PDF
pero idealmente luego soportara todo tipo de documento con texto, la idea general del programa es que uno le pasa el pdf sobre el cual quiere consultar y este te engtrega 
un fragmento de texto literal del pdf donde se responde tu pregunta en base  a una busqueda por similitud y luego tambien utilizamos un agente para dar una respuesta mas concreta.

Tomas Valenzuela- tomasvalenzuelavilches@gmail.com

desarrollo:
	python
	langchain
ejecucion: cd hasta la carpeta en donde se encuentra el ejecutable y luego -streamlit run agentepdf.py