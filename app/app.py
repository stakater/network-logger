
from flask import Flask
nl_app = Flask(__name__)


if __name__ == "__main__":
    nl_app.run(host='0.0.0.0', debug=False)