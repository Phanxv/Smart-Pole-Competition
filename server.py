from flask import json
from flask import request
from flask import Flask

app = Flask(__name__)

@app.route('/webhook', methods = ['POST'])

def api_root() :
    print(json.dumps(request.json, indent=1))
    return "OK"

if __name__ == '__main__' :
    app.run()