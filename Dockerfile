from tensorflow/tensorflow:1.7.0-py3

# Install python dependencies
RUN pip install Flask textblob seaborn matplotlib keras

# download Textblob dataset
RUN python -m textblob.download_corpora

# download Vader dataset
RUN python -m nltk.downloader vader_lexicon

# server port
EXPOSE 5000

WORKDIR /srv

ADD sentiment-api-server.py /srv
ADD static /srv/static

# Add Tini
ENV TINI_VERSION v0.17.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

CMD    ["python", "/srv/sentiment-api-server.py"]