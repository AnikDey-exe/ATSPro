from flask import Flask, request
from flask_cors import CORS, cross_origin
from ats_test3 import run_ats
from atspro import ATSModel
from gensim.models import Word2Vec 

app = Flask(__name__)

model_f = Word2Vec.load('atstweaked2.model')

CORS(app)

@app.route("/")
def entry_point():
    return "Base url"

@app.route("/test", methods=["POST"])
def test():
    model = Word2Vec.load('atstweaked2.model')
    sim = model.wv.similarity("business", "marketing")
    sim_percentage = round((sim)*100, 2)
    print(sim_percentage)
    return {
        "response": sim_percentage
    }

@app.route("/test2", methods=["POST"])
def test2():
    model = Word2Vec.load('atstweaked2.model')
    return {
        "response": "test 2"
    }

@app.route("/test3", methods=["POST"])
def test3():
    sim = model_f.wv.similarity("business", "marketing")
    sim_percentage = round((sim)*100, 2)
    print(sim_percentage)
    return {
        "response": sim_percentage
    }


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