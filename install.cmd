@echo off
echo.

echo Install python dependencies ...
pip install -r requirements.txt
echo.

echo "Download TextBlob data ..."
python -m textblob.download_corpora
echo.

echo Download NLTK Vader data ...
python -m nltk.downloader vader_lexicon
echo.

echo Installation done.
echo.
echo Run the Sentiment Analysis server :
echo.
echo        start python sentiment-api-server.py
echo.
echo Browse :
echo.
echo        http://localhost:5000
echo.
