from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/addition', methods=['GET'])
def addition():
    result = 1 + 1
    return jsonify({"1+1 = ": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
