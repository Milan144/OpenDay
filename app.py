from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/addition', methods=['GET'])
def addition():
    result = 1 + 5
    return jsonify({"1+5 = ": result})

@app.route('/subtraction', methods=['GET'])
def subtraction():
    result = 5 - 1
    return jsonify({"5-1 = ": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
