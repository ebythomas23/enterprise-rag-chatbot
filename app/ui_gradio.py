import gradio as gr
from rag_pipeline import extract_text_from_pdf, chunk_text
from vector_store import index_chunks, query_chunks
from ollama_integration import query_ollama

# Tracks if a document was uploaded and indexed
document_loaded = False

def handle_upload(file):
    global document_loaded
    try:
        text = extract_text_from_pdf(file.name)
        chunks = chunk_text(text)
        index_chunks(chunks)
        document_loaded = True
        return "Document uploaded and processed successfully. You can now ask questions."
    except Exception as e:
        print("[Upload Error]", str(e))
        return f"Error processing document: {str(e)}"

# Respond to user input
# This function retrieves relevant chunks from the vector store and queries the LLM.
# with the user question and the retrieved context,
# It returns the response from the LLM and updates the chat history.
def respond(message, chat_history):
    global document_loaded

    if not document_loaded:
        chat_history.append(("You: " + message, "Please upload a document first."))
        return "", chat_history

    try:
        retrieved_chunks = query_chunks(message)
        context = "\n".join(retrieved_chunks)
        response = query_ollama(message, context)
        chat_history.append(("You: " + message, response))
    except Exception as e:
        chat_history.append(("You: " + message, f"Error: {str(e)}"))

    return "", chat_history

# Build Gradio Blocks UI manually
with gr.Blocks() as demo:
    gr.Markdown("## Enterprise RAG Chatbot")

    with gr.Row():
        file_upload = gr.File(label="Upload PDF Document", file_types=[".pdf"])
        upload_status = gr.Textbox(label="Upload Status", interactive=False)

    file_upload.change(fn=handle_upload, inputs=file_upload, outputs=upload_status)

    chatbot = gr.Chatbot(label="Chat History")
    user_input = gr.Textbox(placeholder="Ask a question about the uploaded document...", label="Your Question")
    state = gr.State([])

    send_btn = gr.Button("Send")

    send_btn.click(fn=respond, inputs=[user_input, state], outputs=[user_input, chatbot])
