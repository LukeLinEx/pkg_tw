import numpy as np
import pandas as pd


from copy import deepcopy
from bson.objectid import ObjectId
from taiwanese.config import *
import taiwanese.back.utils.sheet as sheet


class HandleSubmission(object):
    def __init__(self):
        self.gsheet = sheet.GSheet(config_path)
        self.__spreadsheet_id = spreadsheet_id

    @property
    def spreadsheet_id(self):
        return self.__spreadsheet_id

    def get_submission_lst(self):
        lst = self.gsheet.get_sheet(
            spreadsheet_id=self.spreadsheet_id, sheet_name="submission")

        return lst["values"][0], lst["values"][1:]

    def get_submission_df(self):
        colnames, values = self.get_submission_lst()

        return pd.DataFrame(values, columns=colnames)

    def add_submission(self, week, student_id, submission_time):
        df = self.get_submission_df()
        found = df.loc[
           np.logical_and(df["student_id"]==student_id, df["week"]==week)
        ]

        if found.shape[0] == 0:
            df = df.append(pd.DataFrame([[student_id, week, submission_time]], columns=["student_id", "week", "submission_time"]))
        else:
            df.loc[
                np.logical_and(df["student_id"] == student_id, df["week"] == week), "submission_time"
            ] = submission_time

        values = [df.columns.tolist()] + df.values.tolist()
        self.gsheet.update_sheet(self.spreadsheet_id, "submission", values)


if __name__ == "__main__":
    h = HandleSubmission()
    h.add_submission("20210104", "5fee6c8b5b414b59f9c1992b", "123")
    # df = h.get_submission_df()
    # df = df.append(pd.DataFrame([[1,2,3], [7,8,9]], columns=["student_id", "week", "submission_time"]))
    # df.loc[
    #     np.logical_and(df["student_id"]==1, df["week"]==2), ["week","submission_time"]
    # ] = [5, 6]
    # print([df.columns.tolist(), df.values.tolist()])
