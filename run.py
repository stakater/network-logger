import os
from app.nl_app import nlapp

port = os.environ.get("APP_PORT")
nlapp.run(host='0.0.0.0', debug=False, port=port)