from taiwanese.config import *
from taiwanese.back.student_list import HandleStudentList
from taiwanese.back.submission import HandleSubmission
from flask import Blueprint, render_template, request
from taiwanese.back.utils.drive import GDrive
from taiwanese.back.utils.doc import GDoc

import time
import boto3
from datetime import date, datetime

hw_bp = Blueprint("hw", __name__)

gdrive = GDrive()
gdoc = GDoc()

aws_session = boto3.Session(profile_name='twta')
s3_client = aws_session.client('s3')

@hw_bp.route("/<string:week>/<string:student_id>/", methods=['GET', 'POST'])
def submit(week, student_id):
    hsl = HandleStudentList()
    hsb = HandleSubmission()

    found = [doc for doc in hsl.active if doc[0] == student_id]
    if len(found)==0:
        raise ValueError("The student id is not found")

    name = found[0][1]
    email = found[0][2]

    doc_id = [r for r in gdrive.list_files(material_g_folder_id) if r["name"] == week][0]["id"]
    paragraph = gdoc.load_doc(doc_id)

    if request.method == "POST":
        f = request.files['audio_data']
        tmp_file = "{}/{}_{}.wav".format(output_folder, week, student_id)

        with open(tmp_file, 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        s3_client.upload_file(tmp_file, Bucket="taiwanese", Key="{}/{}".format(week, student_id))
        os.remove(tmp_file)
        hsb.add_submission(week, student_id, str(date.today()))

        return render_template(
            'assignment.html', name=name, week=week, paragraph=paragraph,
            student_id=student_id, equest="POST")
    else:
        return render_template(
            "assignment.html", name=name, week=week, paragraph=paragraph,
            student_id=student_id)


@hw_bp.route("/summary/<string:student_id>/")
def list_old(student_id):
    hsl = HandleStudentList()
    hsb = HandleSubmission()

    df = hsb.get_submission_df()
    df = df.loc[df["student_id"]==student_id]
    values = df.values

    name = [d[1] for d in hsl.axv if d[0]==student_id][0]

    return render_template("summary.html", name=name, values=values)


@hw_bp.route("/submission/<string:student_id>/<string:week>/<string:name>")
def show_old(student_id, week, name):
    tmp_file = "{}/{}{}{}.wav".format(output_folder, week, student_id, str(datetime.now()))
    s3_client.download_file("taiwanese", "{}/{}".format(week, student_id), tmp_file)
    audio_file = tmp_file.split("/")[-1]

    return render_template("listen.html", name=name, student_id=student_id, week=week, audio_file=audio_file)

@hw_bp.route("/delete_tmp/<string:audio_file>", methods=["POST"])
def delete(audio_file):
    time.sleep(5)
    f2brm = "{}/{}".format(output_folder, audio_file)
    os.remove(f2brm)

    return f2brm
