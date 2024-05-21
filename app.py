from flask import Flask, request
from flask_cors import CORS, cross_origin
from ats_test3 import run_ats

app = Flask(__name__)

CORS(app)

@app.route("/")
def entry_point():
    return "Base url"

@app.route("/ats", methods=["GET", "POST"])
def ats():
    if request.method == 'POST':
        content = request.get_json()
        resume_url = content.get('url')
        keywords = content.get('keywords')
        print("r ",resume_url)
        keywords_arr = keywords.split(",")
        result = run_ats(resume_url, keywords_arr)
        print("Eligible ",result)
        return {
            "response": result
        }
    else:
        return {
            "response": "Nothing"
        }

# main driver function
if __name__ == '__main__':
    app.run()