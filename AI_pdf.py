import os
from dotenv import load_dotenv
from genai.extensions.langchain import LangChainInterface
from genai.schemas import GenerateParams
from genai.credentials import Credentials
from langchain.document_loaders import PyPDFLoader

class PDFProcessingError(Exception):
    """Custom exception for errors related to PDF processing."""

def setup_genai_credentials():
    load_dotenv()
    api_key = os.getenv("GENAI_KEY")
    api_url = os.getenv("GENAI_API")
    
    if not api_key or not api_url:
        raise ValueError("Ensure the GENAI_KEY and GENAI_API are set in the environment or .env file.")
    
    return Credentials(api_key, api_endpoint=api_url)

def extract_text_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pdf_content = loader.load()

    if not pdf_content:
        raise PDFProcessingError("PDF is empty or could not be read.")

    try:
        return ' '.join([doc.page_content for doc in pdf_content])
    except AttributeError as e:
        raise PDFProcessingError(f"Failed to extract text from the PDF due to: {e}")

def interact_with_user(extracted_text, langchain_model):
    MAX_TOKENS = 1500

    while True:
        question = input("Ask a question about the PDF (or type 'exit' to quit): ")
        
        if question.lower() == 'exit':
            return

        tokens = extracted_text.split()  # Simple tokenization
        truncated_content = ' '.join(tokens[-MAX_TOKENS:])
        context_question = f"Based on this content from the PDF: {truncated_content}\n{question}"
        
        response = langchain_model(context_question)
        answer = response.text if hasattr(response, "text") else str(response)
        print(f"Answer: {answer}\n")

def main():
    try:
        print("\n------------- Example (LangChain)-------------\n")
        creds = setup_genai_credentials()
        pdf_path = input("Enter the path to the PDF file: ")
        extracted_text = extract_text_from_pdf(pdf_path)

        print("Using GenAI Model expressed as LangChain Model via LangChainInterface:")
        params = GenerateParams(decoding_method="greedy")
        langchain_model = LangChainInterface(model="google/flan-t5-xxl", params=params, credentials=creds)
        interact_with_user(extracted_text, langchain_model)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Exiting...")

if __name__ == "__main__":
    main()
