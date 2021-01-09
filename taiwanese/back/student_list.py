import yaml
from copy import deepcopy
from bson.objectid import ObjectId
from taiwanese.config import *
import taiwanese.back.utils.sheet as sheet


class HandleStudentList(object):
    def __init__(self):
        self.gsheet = sheet.GSheet(config_path)
        with open(config_path, 'r') as stream:
            self.__config = yaml.safe_load(stream)
            self.__spreadsheet_id = self.__config["spread_sheet_id"]["student_list"]
        self.__active = None
        self.__axv = None
        self.get_student_lists()

    @property
    def spreadsheet_id(self):
        return self.__spreadsheet_id

    @property
    def config(self):
        return deepcopy(self.__config)

    @property
    def active(self):
        return deepcopy(self.__active)

    @property
    def axv(self):
        return deepcopy(self.__axv)

    def get_student_lists(self):
        collected = {}
        for key in ("active", "axv"):
            collected[key] = self.gsheet.get_sheet(
                spreadsheet_id=self.spreadsheet_id, sheet_name=key)

        self.__active = collected["active"]["values"]
        self.__axv = collected["axv"]["values"]

    def add_student(self, name, email):
        active_users = {d[2] for d in self.active}
        axv_users = {d[2] for d in self.axv}

        if email in active_users:
            return
        elif email in axv_users:
            record = [d for d in self.axv if d[2] == email][0]
            self.gsheet.append_row(record, self.spreadsheet_id, "active")
            self.get_student_lists()
        else:
            record = [str(ObjectId()), name, email]
            self.gsheet.append_row(record, self.spreadsheet_id, "active")
            self.gsheet.append_row(record, self.spreadsheet_id, "axv")
            self.get_student_lists()

    def archive_student(self, student_id=None, email=None, name=None):
        if student_id:
            print("The student id was provided. Will go with the student_id.")
        elif email:
            if name:
                print("Both email and name were provided. Will go with the email")

            found = [d for d in self.active if d[2] == email]
            if len(found) == 0:
                raise ValueError("The email provided was not found among the active students.")
            elif len(found) > 1:
                raise ValueError("More than one student was found with this email.")
            else:
                student_id = found[0][0]
        elif not name:
            raise ValueError("At least one among the student_id, email, or name should be provided.")
        else:
            found = [d for d in self.active if d[1] == name]
            if len(found) == 0:
                raise ValueError("The email provided was not found among the active students.")
            elif len(found) > 1:
                raise ValueError("More than one student was found with this name.")
            else:
                student_id = found[0][0]

        found = [d for d in self.active if d[0] == student_id]
        if len(found) == 0:
            raise ValueError("The student_id provided was not found among the active students.")
        else:
            idx = [d[0] for d in self.active].index(student_id)

        kept = self.active[idx+1:]
        self.gsheet.update_rows(kept,self.spreadsheet_id, "active", idx + 1)
        self.gsheet.clear_rows(self.spreadsheet_id, "active", idx+1+len(kept))
        self.get_student_lists()
