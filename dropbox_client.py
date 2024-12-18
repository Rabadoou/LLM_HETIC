import dropbox
import PyPDF2

class DropboxClient:
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)

    def list_files(self, folder_path):
        try:
            result = self.dbx.files_list_folder(folder_path)
            return result.entries
        except dropbox.exceptions.ApiError as e:
            print(f"Erreur lors de la récupération des fichiers : {e}")
            return []

    def download_file(self, file_path):
        local_path = f"./{file_path.split('/')[-1]}"  
        try:
            with open(local_path, 'wb') as f:
                metadata, res = self.dbx.files_download(path=file_path)
                f.write(res.content)
            print(f"Fichier téléchargé avec succès : {local_path}")
            return local_path
        except Exception as e:
            print(f"Erreur lors du téléchargement du fichier {file_path}: {e}")
            return None

    def read_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()  
            return text
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier PDF {file_path}: {e}")
            return None
