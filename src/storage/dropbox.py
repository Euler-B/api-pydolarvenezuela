import dropbox
from datetime import datetime
from ._base import Storage
from ..consts import DROPBOX_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_FOLDER

class DropboxStorage(Storage):
    def __init__(self):
        self.client = dropbox.Dropbox(
            DROPBOX_TOKEN, 
            app_key=DROPBOX_APP_KEY, 
            app_secret=DROPBOX_APP_SECRET
        )

        folders = self.client.files_list_folder('').entries
        if DROPBOX_FOLDER not in [folder.name for folder in folders]:
            self.client.files_create_folder(f'/{DROPBOX_FOLDER}')

    def upload(self, file: str):
        date_str = datetime.now().strftime('%Y-%m-%d')
        with open(file, 'rb') as f:
            self.client.files_upload(f.read(), f'/{DROPBOX_FOLDER}/backup_{date_str}.sql')