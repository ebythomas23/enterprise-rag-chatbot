import fitz

def extract_text_from_pdf(file_path):
    #reads the PDF file and extracts text from it
    text =""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chunk_text(text,chunk_size=500, overlap=50):
    #chunks the text into smaller pieces
    chunks=[]
    start =0
    while start<len(text):
        end= min(start+ chunk_size, len(text))
        chunks.append(text[start:end])
        start+= chunk_size-overlap
    return chunks 


#note:
##extract_text_from_pdf: uses PyMuPDF to read PDF pages into a single text string
#chunk_text: splits that text into overlapping segments, helping the model understand context across pages