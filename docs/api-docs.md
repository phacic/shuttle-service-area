# API Documentation

#### Content

- [Overview](#1-overview)
- [Provider](#2-provider)
- [Service Area](#2-service-area)

## 1. Overview

This is a JSON API and as such requests content-type should be set to `application/json`.

All requests are made to the endpoint `http://localhost:5500/`

## 2. Provider

url: `.../providers/`

CRUD operations on Providers are handled by this endpoint

### Create a provider

```shell
curl --location --request POST 'http://localhost:5500/providers/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "VIP",
    "email": "vip@example.com",
    "phone_number": "+233544680391",
    "language": "Twi",
    "currency": "GHC"
}'
```

and the response will look something like

```json
{
    "id": 3,
    "name": "VIP",
    "email": "vip@example.com",
    "phone_number": "+233544680391",
    "language": "Twi",
    "currency": "GHC",
    "status": "A",
    "create_date": "2022-03-08T09:02:46.193070Z",
    "update_date": "2022-03-08T09:02:46.193093Z"
}
```

### List providers

```shell
curl --location --request GET 'http://localhost:5500/providers/'
```

### On a single provider

```shell
curl --location --request DELETE 'http://localhost:5500/providers/3/'
```

Note that the above request (DELETE) request currently only does a soft delete on a provider, meaning it status is
 changed from `Active(A)` to `Inactive(I)`. The other HTTP verbs
(*GET*, *PATCH*, *PUT*) work as expected

## 3. Service Area

url: `.../service-areas/`

CRUD operations on Providers are handled by this endpoint

### Create Service area

```shell
curl --location --request POST 'http://localhost:5500/service-areas/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "provider": 3,
    "name": "Palm-way",
    "price": 22.50,
    "poly": "POLYGON(( -3 -3, 7 20, 14 3, 10 15, -3 -3))"
}'
```

it should return a response like this

```json
{
    "id": 4,
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-3.0, -3.0],
                [7.0,  20.0],
                [14.0, 3.0],
                [10.0, 15.0],
                [-3.0, -3.0]
            ]
        ]
    },
    "properties": {
        "provider": 3,
        "name": "Beach-way",
        "price": "22.50"
    }
}
```

### List Service Areas

```shell
curl --location --request GET 'http://localhost:5500/service-areas/'
```

### On a single Service Area

```shell
curl --location --request DELETE 'http://localhost:5500/service-areas/4/'
```

Note that the above request (DELETE) request currently only does a soft delete on a service-area,
meaning it status is  changed from `Active(A)` to `Inactive(I)`. The other HTTP verbs
(*GET*, *PATCH*, *PUT*) work as expected
