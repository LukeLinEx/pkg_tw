from flask import Flask
from flask import request
from flask import render_template
from taiwanese.hw.homework import hw_bp
from os.path import expanduser

app = Flask(__name__)
app.register_blueprint(hw_bp, url_prefix='/homework')


@app.route("/")
def msg():
    home = expanduser("~")
    return home


@app.route("/index/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('{}/audio.wav'.format(output_path), 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
