import ollama
from config import DROPBOX_ACCESS_TOKEN, DEFAULT_TEMPERATURE
from dropbox_client import DropboxClient

dropbox_client = DropboxClient(DROPBOX_ACCESS_TOKEN)

def get_documents_from_dropbox():
    files = dropbox_client.list_files("/project")
    documents = []
    
    for file_metadata in files:        
        local_path = dropbox_client.download_file(file_metadata.path_display)
        if local_path:
            text = dropbox_client.read_pdf(local_path)
            if text:
                documents.append(text)  
    
    return documents

def ask_without_rag(question):
    try:
        print("Envoi de la question à Ollama sans RAG...")
        response = ollama.chat(
            model="llama3.2",  # Vérifiez que c'est bien le modèle correct
            messages=[{"role": "user", "content": question}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Erreur avec l'API Ollama : {e}")
        return "Erreur lors de la communication avec l'API."

def ask_with_rag(question, documents):
    try:
        print("Envoi de la question à Ollama avec RAG...")
        context = "\n\n".join(documents)
        response = ollama.chat(
            model="llama3.2",  
            messages=[ 
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Question: {question}\nContext: {context}"}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Erreur avec l'API Ollama : {e}")
        return "Erreur lors de la communication avec l'API."

def demo(question, use_rag=False):
    print(f"\nDemande : {question}")
    documents = get_documents_from_dropbox() 
    
    if use_rag: 
        print("\nAvec RAG:") 
        response = ask_with_rag(question, documents)
        print("Réponse avec RAG : ", response)
        print(response)
    else: 
        print("\nSans RAG:") 
        response = ask_without_rag(question)
        print("Réponse sans RAG : ", response)
        print(response)

def main():
    print("Bonjour ! Ce programme va répondre à la question : 'Quelle est la température du corps ?'")
    
    while True:
        choice = input("Voulez-vous utiliser la méthode RAG (avec documents de Dropbox) ? (oui/non) : ").strip().lower()
        if choice in ['oui', 'non']:
            break
        else:
            print("Réponse invalide. Veuillez répondre par 'oui' ou 'non'.")
    
    use_rag = choice == "oui"
    
    question = "Quelle est la température du corps ?"
    demo(question, use_rag)

if __name__ == "__main__":
    main()
