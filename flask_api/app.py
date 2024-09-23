from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "SDPX GROUP 3"

@app.route('/getcode', methods=['GET'])
def getcode():
    return "SDPX GROUP 3 (GETCODE) Date 2021-09-30"


@app.route('/plus/<num1>/<num2>', methods=['GET'])
def plus(num1, num2):
    try:
        num1 = eval(num1)
        num2 = eval(num2)

        results = {
                'plus' : num1 + num2,
            }
    except:
        results = { 'error_msg' : 'Invalid input' }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
