import os
from dotenv import load_dotenv
from genai.extensions.langchain import LangChainInterface
from genai.schemas import GenerateParams
from genai.credentials import Credentials
from langchain.document_loaders import PyPDFLoader

def setup_genai_credentials():
    load_dotenv()
    api_key = os.getenv("GENAI_KEY", None)
    api_url = os.getenv("GENAI_API", None)
    
    if not api_key or not api_url:
        print("Error: Ensure the GENAI_KEY and GENAI_API are set in the environment or .env file.")
        exit()

    return Credentials(api_key, api_endpoint=api_url)

def extract_text_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pdf_content = loader.load()

    try:
        # Assuming 'page_content' is the correct attribute to access the PDF content
        return ' '.join([doc.page_content for doc in pdf_content])
    except AttributeError as e:
        print("Error: Failed to extract text from the Document objects.")
        available_attributes = dir(pdf_content[0]) if pdf_content else []
        print(f"Available attributes/methods: {available_attributes}")
        exit()

def interact_with_user(extracted_text, langchain_model):
    MAX_TOKENS = 1500

    while True:
        question = input("Ask a question about the PDF (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        
        tokens = extracted_text.split()  # Simple tokenization
        truncated_content = ' '.join(tokens[-MAX_TOKENS:])

        context_question = f"Based on this content from the PDF: {truncated_content}\n{question}"
        response = langchain_model(context_question)
        print(f"Answer: {response}\n")

def main():
    print("\n------------- Example (LangChain)-------------\n")
    creds = setup_genai_credentials()

    pdf_path = input("Enter the path to the PDF file: ")
    extracted_text = extract_text_from_pdf(pdf_path)

    # Ask the user if they want to view the PDF content
    view_content = input("Would you like to view the contents of the PDF? (yes/no): ").lower()
    if view_content == "yes":
        print("\n------ Begin PDF Content ------\n")
        print(extracted_text)
        print("\n------ End PDF Content ------\n")

    print("Using GenAI Model expressed as LangChain Model via LangChainInterface:")
    params = GenerateParams(decoding_method="greedy")
    langchain_model = LangChainInterface(model="google/flan-t5-xxl", params=params, credentials=creds)

    interact_with_user(extracted_text, langchain_model)

    print("Exiting...")

if __name__ == "__main__":
    main()
