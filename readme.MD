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

## API description

### Add *tiny_url* into database
POST request to **/shorten** with a body in format:
```
{
    "url": "https://www.example.com/",
    "shortcode": "abn123"
}
```
This will create a record in the database. 
When no shortcode provided a random shortcode for the provided url. 
The shortcode has a length of 6 characters and will contain only
alphanumeric characters or underscores.
In case of successful POST reqeust you will receive response with status 201 and the following body:
```
{
    "shortcode": "abn123"
}
```

Otherwise, you will get one of the next errors:

| Error |               Info                |
|-------|:---------------------------------:|
| 400   |          Url not present          |
| 409   |     Shortcode already in use      |
| 412   | The provided shortcode is invalid |

### Get *tiny_url* by *original_url*

GET request to **/<tyni_url>**.

Returns http status 302 with the Location header containing the original url.

| Error |        Info         |
|-------|:-------------------:|
| 404   | Shortcode not found |

### Get stats by *tiny_url*

GET request to **/<tyni_url>/stats**.

Returns http status 200 with the following body:

```
{
    "created": "2017-05-10T20:45:00.000Z",
    "lastRedirect": "2018-05-16T10:16:24.666Z",
    "redirectCount": 6
}
```

*created* contains the creation datetime of the shortcode (in ISO8601)

*lastRedirect* contains the datetime of the last usage of the shortcode (in ISO8601)

*redirectCount* indicates the number of times the shortcode has been used

| Error |        Info         |
|-------|:-------------------:|
| 404   | Shortcode not found |


#### TBD

1. Add cashing (Redis)
2. Add more tests
3. Add more logs
4. Add statistics