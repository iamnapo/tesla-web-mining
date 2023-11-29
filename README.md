# Part 2 of the Web Data Mining course @ DWS MSc

[![Netlify Status](https://api.netlify.com/api/v1/badges/d2a44cad-ed48-404e-b976-cdfbe125a320/deploy-status)](https://tesla.iamnapo.me/)

<h2 align="center"><a href="https://github.com/iamnapo/tesla-web-mining/raw/main/src/assets/report.pdf" download>Our report</a></h2>

## Repository structure

- In the root of this repository there are the required files to deploy the website. There is already an online version available at Netlify. (Just press the button above)
- In the [`dataset/`](./dataset) folder there is a dump of the MongoDB database that we used for our analyses.
- In the [`analysis-scripts/`](./analysis-scripts) folder there are all the various scripts that we used for our analyses.

## Usage

All of the steps below require that you have already installed:

- [Node.js 12.13 or later](https://nodejs.org/en/)
- [Python 3.6 or later](https://www.python.org/)
- [MongoDB 4.0 or later](https://www.mongodb.com)

### Website

- Install depencencies:

  ```sh
  npm i
  ```

- Run the development server:

  ```sh
  npm run develop
  ```

- Or build and serve the production bundle:

  ```sh
  npm run build
  npm run serve
  ```

### Mongo dataset

- Download the dump from the [`dataset/`](./dataset) folder.
- Join the three parts of the .gz file into one, using something like:
  - Windows: `type twitter_search.bson.gz.* > twitter_search.bson.gz`
  - Linux/MacOS: `cat twitter_search.bson.gz.* > twitter_search.bson.gz`
- Use the [`mongorestore`](https://docs.mongodb.com/manual/reference/program/mongorestore/) command, in conjuction with the `--gzip` option.

### Python scripts

- Install dependencies from [`analysis-scripts/requirements.txt`](./analysis-scripts/requirements.txt)
- Download necessary nltk files. In a python3 shell:

  ```python
  >>> import nltk
  >>> nltk.download('stopwords')
  >>> nltk.download('punkt')
  ```

- Make sure to set each script's required environment variables before executing it!
- Also, again, make sure that you have at least 3.6 Python, because these script use [f literals](https://www.python.org/dev/peps/pep-0498/).
