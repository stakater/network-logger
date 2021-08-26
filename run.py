import os
from app.nl_app import nlapp


port = os.environ.get("APP_PORT")
https = os.environ.get("HTTPS")
print(port, https)
if https:
    nlapp.run(host='0.0.0.0', debug=False, port=port, ssl_context='adhoc')
else:
    nlapp.run(host='0.0.0.0', debug=False, port=port)