# Raggy App

A minimal implimintation of RAG Model for questions answering.

## Requirements

- Python 3.8 or later.

### Install Python  using MiniConda

1) Download and Install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/install)
2) Create a new environment using the following command:
```bash
$ conda create -n raggy python=3.8
```
3) Activate the created environment using the command
```bash
$ conda activate raggy
```
### (Optional) Setup your command line for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```
You need to re-activate your env

## Installation

### Install the required packages
```bash
$ pip install -r requirements.txt
```
### Setup the environment variables
```bash
$ cp .env.example .env
```
Set your environment variables in the .env file. Like OPENAI_API_KEY value.

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```
*important:* DO not forget to update .env with your credentials

```bash
sudo docker compose up -d
```


## Run the FastAPI server
use the following command to run the server with these settings (reload enabled, accept ip's, and port 5000)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection
find the collection file in [assets/raggy-app.postman_collection.json](assets/raggy-app.postman_collection.json)