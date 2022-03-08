# shuttle-service-area

Providers and their Service-Areas backend

## Running server

Docker needs to be installed to run the server. Run the following command to start the server

```shell
docker-compose up -d
```

The server is accessible on `http://localhost:5500/`

## Running Tests

```shell
 docker-compose run --rm -e TEST_ENV=1 web pytest -v
```

## API Docs

The API documentation is [located here](docs/api-docs.md).

## Swagger Docs

For swagger (OpenAPI) documentation

`http://localhost:5500/docs/`


## Todo

- Caching (To improve performance)