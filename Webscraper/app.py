from flask import Flask, jsonify, render_template 
from scraping import scrape
from flask import request
from flask import json
app = Flask(__name__)
@app.route('/')
def index():
    data = str(request.args.get('query'))
    data = scrape(data)
    # response = app.response_class(
        # response=json.dumps(data),
        # status=200,
        # mimetype='application/json'
    # )
    # return response
    return render_template("index.html", datas = data) 
if __name__ == "__main__":
    app.run(debug=True)