from copy import deepcopy
import yaml
from taiwanese.back.utils.gapi_connection import get_sheet_service


class GSheet(object):
    def __init__(self, config_path):
        with open(config_path, 'r') as stream:
            self.__config = yaml.safe_load(stream)

        self.__service = self.get_service()

    def get_service(self):
        cred_path = self.config["credentials"]["google"]
        return get_sheet_service(cred_path)

    @property
    def config(self):
        return deepcopy(self.__config)

    @property
    def service(self):
        return self.__service

    def append_row(self, row, spreadsheet_id, sheet_name):
        value_input_option = "USER_ENTERED"

        body = {'values': [row]}
        self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=sheet_name,
            valueInputOption=value_input_option, body=body).execute()

    def update_row(self, row, spreadsheet_id, sheet_name, nth):
        value_input_option = "RAW"

        body = {'values': [row]}
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range="{}!{}:{}".format(sheet_name, nth, nth),
            valueInputOption=value_input_option, body=body
        ).execute()

    def update_rows(self, rows, spreadsheet_id, sheet_name, nth):
        value_input_option = "RAW"

        end = nth -1 + len(rows)

        body = {'values': rows}
        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range="{}!{}:{}".format(sheet_name, nth, end),
            valueInputOption=value_input_option, body=body
        ).execute()

    def update_sheet(self, spreadsheet_id, sheet_name, values):
        body = {
            "values": values}

        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=sheet_name,
            valueInputOption="USER_ENTERED", body=body).execute()

    def clear_rows(self, spreadsheet_id, sheet_name, nth, end=None):
        if not end:
            end = nth

        self.service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range="{}!{}:{}".format(sheet_name, nth, end)
        ).execute()

    def get_sheet(self, spreadsheet_id, sheet_name):
        sheet = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=sheet_name).execute()

        return sheet
