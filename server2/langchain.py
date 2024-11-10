import os
import io
import requests
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)


def get_pdf_text(pdf_path):
    text = ""
    
    try:
        if pdf_path.startswith("http"):
            
            response = requests.get(pdf_path)
            response.raise_for_status()
            pdf_reader = PdfReader(io.BytesIO(response.content))
        else:
           
            with open(pdf_path, "rb") as file:
                pdf_reader = PdfReader(file)
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:  
                text += page_text

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    
    if not chunks:
        print("Warning: No text chunks generated. Please check the PDF content.")
    
    return chunks


def get_vector_store(text_chunks):
    if not text_chunks:
        print("Error: No text chunks to process for vector store creation.")
        return None
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    try:
        if hasattr(embeddings, "embed_documents"):
            all_embeddings = embeddings.embed_documents(text_chunks)
            if not all_embeddings:
                raise ValueError("Failed to generate embeddings.")
        else:
            raise AttributeError("The embeddings model does not support batch embedding.")
        
        os.makedirs("faiss_index", exist_ok=True)
        
        
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        print("FAISS vector store created and saved.")
        return vector_store

    except Exception as e:
        print("Error generating or saving embeddings:", e)
        return None


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    If the answer is not in the provided context, respond with "Answer is not available in the context."
    
    Context:\n {context}\n
    Question: {question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print("Error loading FAISS index:", e)
        return "Unable to load FAISS index; please check if it was saved correctly or if embeddings are configured properly."
    

    docs = new_db.similarity_search(user_question)
    

    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    return response


def pdf_qa_function(question, file_path): 
  
    print(file_path)
    raw_text = get_pdf_text(file_path)
    if not raw_text.strip():
        return {"output_text":"No text extracted from the PDF. Please check the file content."}
    

    text_chunks = get_text_chunks(raw_text)
    

    if get_vector_store(text_chunks) is None:
        return {"output_text":"Failed to create FAISS vector store. Please check embeddings or API configuration."}
    

    if question:
        return user_input(question)
    else:
        return {"output_text":"No question provided. Please provide a question to get an answer."}


