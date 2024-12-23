FROM python:3.12-slim-bookworm

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY static/styles/style.css /static/styles/style.css

COPY static/favicon.ico /static/favicon.ico

COPY static/layer_image.png /static/layer_image.png

COPY templates/index.html /templates/index.html

COPY app.py app.py

COPY config.py config.py

COPY models.py models.py

COPY scraper.py scraper.py

CMD ["python3", "app.py"]