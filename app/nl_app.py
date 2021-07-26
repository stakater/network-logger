from flask import Flask

nlapp = Flask(__name__)

from .views import *

