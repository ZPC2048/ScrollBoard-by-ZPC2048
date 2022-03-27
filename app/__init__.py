from flask import Flask

app = Flask(__name__)
app.secret_key = b"aslgk][2%#@"

from app import routes