from waitress import serve
from models import init_map
from scraper import postcode_findr, rand_postcode
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        if request.form["Postcode Lookup"] == "Lookup Postcode":
            postcode_lookup = request.form["Postcode"]
            data = postcode_findr(lookup=postcode_lookup)

            map_html = init_map(data)

            return render_template("index.html", map=map_html)

    return render_template("index.html")


if __name__ == "__main__":

    serve(app, host="0.0.0.0", port=5555)
