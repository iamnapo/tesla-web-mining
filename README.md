# Part 2 of the Web Data Mining course @ DWS MSc

[![Netlify](https://api.netlify.com/api/v1/badges/d2a44cad-ed48-404e-b976-cdfbe125a320/deploy-status)](https://twitter-analysis.netlify.com)

## Repository structure

- In the root of this repository there are the required files to deploy the website. There is already an online version available at Netlify. (Just press the button above)
- In the `dataset/` folder there is a dump of the MongoDB database that we used for our analyses.
- In the `analysis-scripts/` folder there are all the various scripts that we used for out analyses.

## Usage

All of the steps below require that you have already installed:

- [Node.js 10.4 or later](https://nodejs.org/en/)
- [Python 3.6 or later](https://www.python.org/)
- [MongoDB 4.0 or later](https://www.mongodb.com)

### Website

- Install depencencies:

  ```sh
  $ npm i
  ```

- Run the development server:

  ```sh
  $ npm run develop
  ```

- Or build and serve the production bundle:

  ```sh
  $ npm run build
  $ npm run serve
  ```

### Mongo dataset

- Download the dump from the [`dataset/`](./dataset) folder.
- Use the [`mongorestore`](https://docs.mongodb.com/manual/reference/program/mongorestore/) in conjuction with the `--gzip` option.
