# TinyURL

The project is using Django, Docker, Gunicorn and Postgres.


## How to run
1. Make sure you have [Docker](https://docs.docker.com/engine/install/)
2. Clone the repository
```sh
$ git clone https://github.com/0pa/tinyURL.git
$ cd tinyUR
```

### Development

The application uses the default Django server for the development.
1. To run application in the dev mod
 ```sh
 $ docker-compose up -d --build
 ```

Tests and migrations will be run before the application launching. 

Test it out at [http://localhost:8000](http://localhost:8000).

2. To stop application use
 ```sh
 $ docker-compose down
 ```
### Production

Uses Gunicorn as HTTP Server. 

For the first run it is needed to run migrations manually:
```sh
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```
Then you can run the application:
```sh
$ docker-compose -f docker-compose.prod.yml up -d --build
```
Rerun containers will not affect data. The application is available by [http://localhost:8000](http://localhost:8000).

Stop and remove containers, networks:
```sh
$ docker-compose down
```

#### TBD

1. Add cashing (Redis)
2. Add more tests
3. Add more logs
4. Add statistics