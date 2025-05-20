import gradio as gr
from rag_pipeline import extract_text_from_pdf,chunk_text
from vector_store import index_chunks,query_chunks
from ollama_integration import query_ollama

#Track whether a document has been processed
document_loaded = False

#parses and chunks the PDF, indexes chunks to ChromaDB
def handle_upload(file):
    global document_loaded
    try:
        #extract text from the PDF
        text = extract_text_from_pdf(file.name)
        #chunk the text into smaller pieces
        chunks = chunk_text(text)
        #index the chunks to ChromaDB
        index_chunks(chunks)
        document_loaded = True
        return "Document uploaded and processed successfully. You can now ask Questions"
    except Exception as e:
        return f"Error processing document: {str(e)}"
    
def chat_with_bot(message, history):
    if not document_loaded:
        return "Please upload a document first.", history
    try:
        retrived_chunks = query_chunks(message)
        context ="\n".join(retrived_chunks)  
        response= query_ollama(message,context)
        history.append((message, response))
        return "", history
    except Exception as e:
        return f"Error: {str(e)}", history
    
#create the Gradio interface
demo = gr.Blocks()

with demo:
    gr.Markdown("##Enterprise RAG Chatbot")
 
    with gr.Row():
        file_upload =gr.File(label="Upload PDF Document", file_types=[".pdf"])
        upload_status = gr.Textbox(label="Upload Status", interactive=False)


    file_upload.change(fn=handle_upload, inputs=file_upload, outputs=upload_status)

    gr.ChatInterface(fn=chat_with_bot, chatbot=True)