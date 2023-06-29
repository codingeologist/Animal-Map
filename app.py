from models import init_map
from scraper import postcode_findr
from config import DEBUG, ENV
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.config['ENV'] = ENV


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        postcode_lookup = request.form['Postcode']
        data = postcode_findr(lookup=postcode_lookup)

        map_html = init_map(data)

        return render_template('index.html', map=map_html)

    return render_template('index.html')


if __name__ == '__main__':

    app.run()
