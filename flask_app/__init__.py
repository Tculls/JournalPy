from flask import Flask



app = Flask(__name__)

app.secret_key = "No forget python pls"

# flash messages get saved into session