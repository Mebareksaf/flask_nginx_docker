from flask import Flask

app = Flask(__name__)

#we need to import views
from app import views

