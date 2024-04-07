# Fastapi, Postgresql, Redis, Apache ab report, Docker compose


## File Structure
```
├─ apache-ab-reports >>> outputs added
├─ apps >>> app, event, story, user models, api routes and services (db related methods)
├─ core >>> fastapi environment variables, utils, database, redis configs
├─ docker >>> fastapi and apache ab dockerfiles here, postgre, pgadmin and redis already installing from official image
├─ scripts >>> created initial data script on load, the same records given in the case
├─ tests >>> conftest for general configs and overrides during test, app and story tests.
```

### Dependencies
```
healthcheck feature requires Docker 1.12.0+.

Docker version 24.0.2, build cb74dfc
Docker Compose version v2.19.1
Docker Desktop version 4.21.1 (114176)
```

## Project setup
```
docker-compose up -d
```

#### On local
```

(If you want to run on local, remove the ab and app services in the docker compose)
postgre, pgadmin, redis will be installed by docker-compose
docker-compose up -d


<Create virtualenv>
$ mkdir venv && cd venv
$ virtualenv .
$ cd ..
$ source venv/Scripts/activate
$ pip install -r requirements.txt
< Then run fastapi (entrypoint.sh)>
$ uvicorn main:application --reload --host 0.0.0.0 --port 8001

```

### API & Swagger
```
default fastapi port 8001
[swagger](http://127.0.0.1:8001/docs) check the openapi swagger page and test the endpoints
[pgAdmin](http://127.0.0.1:5050/browser/) postgresql dashboard

```

### Check redis example
```
docker exec -it <redis_container_id>
redis-cli
keys *
get "http://127.0.0.1:8001/stories/token1"
```

### Run tests and coverage
```
pytest tests

coverage run -m pytest
coverage report
coverage html
```
