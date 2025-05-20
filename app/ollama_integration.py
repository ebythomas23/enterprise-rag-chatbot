import ollama

#combines user query and context to create a prompt ans send it to the llm , and returns the response
def query_ollama(query,context, model_name="llama3.2:1b"):
  prompt=f"""
    Use the following contect to answer the question

    Context: {context}
    Question: {query}
    Answer:
  """
  #send the prompt to the LLM and get the response
  try:
    response= ollama.chat(model=model_name,
                          message=[{"role":"user","content":prompt}])
    return response['message']['content']
  except Exception as e:
    return f"Error:{str(e)}"
  


  #this is the Generation part of RAG.
  #It takes the user query and the context (retrieved from the vector store) and sends it to the LLM (Ollama) to generate a response.
 #The function constructs a prompt by combining the context and the query, and then sends it to the LLM using the ollama.chat method.    
 #The response from the LLM is returned as the final answer to the user.