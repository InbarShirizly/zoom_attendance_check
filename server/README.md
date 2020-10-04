# zoom-attendance-check API

API doc can be found [here](https://documenter.getpostman.com/view/4335694/TVRg694k)

## Requirements
1. Install python 3 and pip
2. `pip install -r requirements.txt`
3. `python run.py`

API will be running now at: `http://localhost:5000`

## Project structure
The server code is inside server package, and can be runned with the external module `run.py`.
We decided to use `flask-restful` extenstion in order to create the endpoints, and `flaks-sqlalchemy` in order to create the database.

The inside the `server` package is organzied into the following sub-packages:

- `api` - package which is responsible for the api endpoints
- `utils` - general utils for the application

also there are:

- `models.py` - ORM models for the database
- `config.py` - genreal settings for the application