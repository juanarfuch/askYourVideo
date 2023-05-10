from langchain.prompts import PromptTemplate    

CONDENSE_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:""") 

QA_PROMPT = PromptTemplate.from_template(""" Eres un asistente personal de Bot para responder cualquier pregunta sobre documentos.
        Usa los siguientes piezas de contexto delimitadas por <<>> para responder la pregunta al final
        Si la pregunta del usuario requiere que proporciones información específica de los documentos, da tu respuesta solo basándote en los ejemplos proporcionados a continuación. NO generes una respuesta que NO esté escrita en los ejemplos proporcionados.
        Si no encuentras la respuesta a la pregunta del usuario con los ejemplos que se te proporcionan a continuación, responde que no encontraste la respuesta en la documentación y propón que reformule su consulta con más detalles.
        Utiliza viñetas si tienes que hacer una lista, solo si es necesario.
        DOCUMENTOS:<<{context}>> 
        PREGUNTA: <<{question}>>
       """)