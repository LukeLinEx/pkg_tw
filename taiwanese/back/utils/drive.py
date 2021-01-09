import yaml
from copy import deepcopy
from taiwanese.config import *
from taiwanese.back.utils.gapi_connection import get_drive_service


class GDrive(object):
    def __init__(self):
        with open(config_path, 'r') as stream:
            self.__config = yaml.safe_load(stream)

        self.__service = self.get_service()

    def get_service(self):
        cred_path = self.config["credentials"]["google"]
        return get_drive_service(cred_path)

    @property
    def config(self):
        return deepcopy(self.__config)

    @property
    def service(self):
        return self.__service

    def list_files(self, folder_id):
        #         dservice = get_drive_service(cred_path)
        all_files = []
        page_token = None
        while True:
            response = self.service.files().list(
                q="parents in '{}'".format(folder_id), spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token).execute()
            for file in response.get('files'):
                # Process change
                all_files.append(file)
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return all_files
