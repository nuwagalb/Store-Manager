from flask import Flask, render_template

api = Flask(__name__)

@api.route("/")
def index():
    """returns the index.html template"""
    return render_template('index.html')

if __name__ == "__main__":
    api.run(debug=True)   
