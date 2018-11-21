# py-sentiment-api-server
Sentiment Analysis API server based on TextBlob and NLTK Vader components ( Docker container provided )

## Description

This component provide an web API provided sentiment analysis based on several well known components :

- TextBlob
- TextBlob with Naive Bayses analyser
- NLTK Vader component

For each component, and server endpoint is implemented where you simply have to post the text to be analysed :
- /api/textblob
- /api/textblob/naive-bayes
- /api/vader

## Open-source license

  Apache License Version 2.0

## Install and Run

The server is implemented on Python using Flask, NLTK and TextBlob components.

### With docker

#### use provided docker image
```
docker run -p 5000:5000 -d evrycollin/py-sentiment-api-server:latest
```
#### docker-compose.yml
```
sentiment-api:
  image: evrycollin/py-sentiment-api-server:latest
  container_name: sentiment-api
  ports:
  - "5000:5000"
```

#### use your own docker image

- build

```
  docker build -t py-sentiment-api-server .
```

- run the server

```
  docker run -p 5000:8000 -d py-sentiment-api-server
```


### On Windows

- install

```
  install.cmd
```
- run the server

```
  start python sentiment-api-server.py
```

### On Linux / Mac-OS

- install

```
  install.sh
```
- run the server

```
  python sentiment-api-server.py
```


### Manual setup

```
pip install -r requirements.txt
python -m textblob.download_corpora
python -m nltk.downloader vader_lexicon

```

## Usage

### Provided webUI

A basic webui is provided in order to quickly get and compare sentiment analysis for each components.

Once the server is started, browse to  [http://localhost:5000](http://localhost:5000)

![Screenshot](screenshot-1.png)

### Curl

```
  # Textblob :
  curl -XPOST -H "Content-Type: application/json" -d "I'm happy" http://localhost:5000/api/textblob
  
  # Textblob (Naive Bayses) :
  curl -XPOST -H "Content-Type: application/json" -d "I'm happy" http://localhost:5000/api/textblob/naive-bayes
  
  # Vader :
  curl -XPOST -H "Content-Type: application/json" -d "I'm happy" http://localhost:5000/api/vader
```

### Java

```
  CloseableHttpClient httpClient = HttpClients.createDefault();
  HttpPost post = new HttpPost(endpoint);
  post.setHeader("Content-Type", "application/json; charset=utf-8");
  post.setEntity(new StringEntity("I'm happy");
  try (CloseableHttpResponse res = httpClient.execute(post)) {
    String sentiment = IOUtils.toString(res.getEntity().getContent(), StandardCharsets.UTF_8);
    System.out.println(sentiment);
  }
```

### JQuery

```
    $.ajax({
      url: '/api/vader',
      type: 'POST',
      contentType: 'application/json',
      data: 'I am happy',
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      success: function(data, status) {
        console.log(data)
      }
    })
```

## Performances

On single computer, achieved and average of 400 results per sec

![Hello World](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAAUCAAAAAAVAxSkAAABrUlEQVQ4y+3TPUvDQBgH8OdDOGa+oUMgk2MpdHIIgpSUiqC0OKirgxYX8QVFRQRpBRF8KShqLbgIYkUEteCgFVuqUEVxEIkvJFhae3m8S2KbSkcFBw9yHP88+eXucgH8kQZ/jSm4VDaIy9RKCpKac9NKgU4uEJNwhHhK3qvPBVO8rxRWmFXPF+NSM1KVMbwriAMwhDgVcrxeMZm85GR0PhvGJAAmyozJsbsxgNEir4iEjIK0SYqGd8sOR3rJAGN2BCEkOxhxMhpd8Mk0CXtZacxi1hr20mI/rzgnxayoidevcGuHXTC/q6QuYSMt1jC+gBIiMg12v2vb5NlklChiWnhmFZpwvxDGzuUzV8kOg+N8UUvNBp64vy9q3UN7gDXhwWLY2nMC3zRDibfsY7wjEkY79CdMZhrxSqqzxf4ZRPXwzWJirMicDa5KwiPeARygHXKNMQHEy3rMopDR20XNZGbJzUtrwDC/KshlLDWyqdmhxZzCsdYmf2fWZPoxCEDyfIvdtNQH0PRkH6Q51g8rFO3Qzxh2LbItcDCOpmuOsV7ntNaERe3v/lP/zO8yn4N+yNPrekmPAAAAAElFTkSuQmCC)
