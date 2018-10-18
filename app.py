from flask import Flask, render_template, request

api = Flask(__name__)

@api.route("/")
def index():
    """returns the index.html template"""
    role = request.args.get('role')

    if not role:
        role = "Visitor"

    return render_template('index.html', role=role)
if __name__ == "__main__":
    api.run(debug=True)
