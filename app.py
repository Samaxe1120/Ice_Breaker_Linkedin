from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from ice_breaker import ice_break_with

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route(rule= "/process", methods=["POST"])

def process():
    name = request.form["name"]
    summary_obj, profile_pic_url = ice_break_with(name=name)
    summary_obj = (summary_obj.model_dump())
    return jsonify(
        {
            "summary": summary_obj['summary'],
            "facts": summary_obj['facts'],
            "photoUrl": profile_pic_url
        }
    )
if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True)