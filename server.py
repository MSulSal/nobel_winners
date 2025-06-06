from flask import Flask, render_template

app = Flask(__name__)

winners = [
    {"name": "Albert Einstein", "category": "Physics"},
    {"name": "V.S. Naipaul", "category": "Literature"},
    {"name": "Dorothy Hodgkin", "category": "Chemistry"},
]


@app.route("/winners")
def winners_list():
    return render_template("testj2.html", heading="A little winners list", winners=winners)

if __name__ == "__main__":
    app.run(port=8000, debug=True)