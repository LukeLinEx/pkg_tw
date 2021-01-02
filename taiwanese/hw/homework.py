from taiwanese.config import *
from flask import Blueprint, render_template, request

hw_bp = Blueprint("hw", __name__)

output_path = "/home/ubuntu/pkg_tw/taiwanese/output"


@hw_bp.route("/<string:week>/<string:student_id>/", methods=['GET', 'POST'])
def submit(week, student_id):
    if request.method == "POST":
        f = request.files['audio_data']
        tmp_file = "{}/{}.wav'".format(output_path, student_id)

        with open(tmp_file, 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")
