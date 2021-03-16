import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive']

def connect():
    
    creds = None
    # valida se já existe em cache o arquivo de token.json 
    # para iniciar a conexão sem abrir a janela do google
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # se o arquivo não existir, iniciar a autenticação do começo
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # salva o arquivo de teste para a proxima conexão
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    logging.info('Iniciando conexão com o gdrive')
    gdrive_instance = build('drive', 'v3', credentials=creds)
    return gdrive_instance

def find_files(gdrive_instance, filename):

    logging.info(f'Buscando arquivos com o nome {filename}')
    results = gdrive_instance.files().list(
        # Filtro considerando seguintes informações:
        # Nome do arquivo -> name contains 'acervo'
        # Arquivos fora da lixeira -> trashed = false
        # Remove as pastas da busca -> mimeType != 'application/vnd.google-apps.folder'
        q=f"name contains '{filename}' and trashed = false and mimeType != 'application/vnd.google-apps.folder'",
        pageSize=10, 
        fields="nextPageToken, files(id, name)").execute()
    
    files = results.get('files', [])

    logging.info(f'{len(files)} arquivos encontrados')

    return files

def download_file(gdrive_instance, file):
    import io
    from googleapiclient.http import MediaIoBaseDownload
    
    logging.info(f'Baixando arquivo {file["name"]}')

    request = gdrive_instance.files().get_media(fileId=file['id'])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        logging.debug("Download %d%%." % int(status.progress() * 100))

    return fh