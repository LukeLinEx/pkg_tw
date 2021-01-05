from taiwanese.config import *
from taiwanese.back.student_list import HandleStudentList
from flask import Blueprint, render_template, request
from taiwanese.back.utils.drive import GDrive
from taiwanese.back.utils.doc import GDoc

import boto3
from botocore.exceptions import ClientError

hw_bp = Blueprint("hw", __name__)
hsl = HandleStudentList(config_path)
gdrive = GDrive(config_path)
gdoc = GDoc(config_path)

aws_session = boto3.Session(profile_name='twta')
s3_client = aws_session.client('s3')

@hw_bp.route("/<string:week>/<string:student_id>/", methods=['GET', 'POST'])
def submit(week, student_id):
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

        return render_template(
            'assignment.html', name=name, week=week, paragraph=paragraph,
            student_id=student_id, equest="POST")
    else:
        return render_template(
            "assignment.html", name=name, week=week, paragraph=paragraph,
            student_id=student_id)


@hw_bp.route("/thank/")
def thank():
    return render_template("thank.html")

