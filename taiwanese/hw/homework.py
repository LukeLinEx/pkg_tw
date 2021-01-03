from taiwanese.config import *
from flask import Blueprint, render_template, request

hw_bp = Blueprint("hw", __name__)


@hw_bp.route("/<string:week>/<string:student_id>/", methods=['GET', 'POST'])
def submit(week, student_id):
    if request.method == "POST":
        f = request.files['audio_data']
        tmp_file = "{}/{}.wav".format(output_folder, student_id)

        with open(tmp_file, 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('index.html', student_id=student_id, equest="POST")
    else:
        return render_template("index.html", student_id=student_id)
