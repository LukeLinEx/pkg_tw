from taiwanese.config import *
from taiwanese.back.student_list import HandleStudentList
from flask import Blueprint, render_template, request

hw_bp = Blueprint("hw", __name__)
hsl = HandleStudentList(config_path)

@hw_bp.route("/<string:week>/<string:student_id>/", methods=['GET', 'POST'])
def submit(week, student_id):
    found = [doc for doc in hsl.active if doc[0] == student_id]
    if len(found)==0:
        raise ValueError("The student id is not found")

    name = found[0][1]
    email = found[0][2]

    if request.method == "POST":
        f = request.files['audio_data']
        tmp_file = "{}/{}.wav".format(output_folder, student_id)

        with open(tmp_file, 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('assignment.html', name=name, week=week, student_id=student_id, equest="POST")
    else:
        return render_template("assignment.html", name=name, week=week, student_id=student_id)
