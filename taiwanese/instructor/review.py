from flask import Blueprint, render_template
from itertools import groupby
import pandas as pd
from taiwanese.back.submission import HandleSubmission
from taiwanese.back.student_list import HandleStudentList

rv_bp = Blueprint("rv", __name__)


@rv_bp.route("/")
def summary():
    hsb = HandleSubmission()
    sub = hsb.get_submission_df()

    hsl = HandleStudentList()
    students = pd.DataFrame(hsl.axv[1:], columns=hsl.axv[0])

    output = sub.merge(students, on="student_id").sort_values(["week", "name"])
    output["ref"] = "/homework/submission/" + output[["student_id", "week", "name"]].agg('/'.join, axis=1)

    lst = list(
        output[['week', 'name', 'ref']].groupby("week"))

    return render_template("instructor_summary.html", lst=lst)


def test():
    hsb = HandleSubmission()
    sub = hsb.get_submission_df()

    hsl = HandleStudentList()
    students = pd.DataFrame(hsl.axv[1:], columns=hsl.axv[0])

    output = sub.merge(students, on="student_id").sort_values(["week", "name"])
    output["ref"] = "/homework/submission/" + output[["student_id", "week", "name"]].agg('/'.join, axis=1)

    lst = list(
        output[['week', 'name', 'ref']].groupby("week")
    )
    return lst


if __name__ == "__main__":
    a = test()
    for k, v in a:
        print(k)
        print(v.values)
        print("\n")
