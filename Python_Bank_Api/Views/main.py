import logging
from flask import Flask, jsonify
from flask import Flask, request
from Python_Bank_Api.Views.account_routes import create_account_route
from Python_Bank_Api.Views.user_routes import create_user_route

app: Flask = Flask(__name__)

@app.route("/")
def hello_world():
    return jsonify({"about": "Hello World"})


logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


create_user_route(app)
create_account_route(app)



if __name__ == '__main__':
    app.run(debug=True)
