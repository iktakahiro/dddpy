# Python DDD example using FastAPI

*NOTE: This repository is an example to explain 'how to implement DDD architecture on Python web applicaiton'. If you will to use this as a reference, add your implementation of authentication and security before deploying to the real world!!*


## Code Architecture

For this implementation, I've adopted the [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/).

Directory structure:

```tree
├── dddpy
│   ├── domain
│   │   └── book
│   │       ├── book.py
│   │       └── book_repository.py
│   ├── infrastructure
│   │   └── sqlite
│   │       ├── book
│   │       │   ├── book_dto.py
│   │       │   └── book_repository.py
│   │       └── database.py
│   ├── presentation
│   │   └── schema
│   │       └── book
│   │           └── book_schema.py
│   └── usecase
│       └── book
│           └── book_usecase.py
├── main.py
└── tests
```

### DTO (Data Transfer Object) 

DTO (Data Transfer Object) is a good practice to isolate domain objects from the infrastructuer layer.

On a minimum MVC architecture, models often extend a base class provided by a O/R Mappaer. But in that case, the domain layer would be dependent on the outer layer.

To solve this problem, we can simply set two rules:

1. A domain object **DOES NOT** extend SqlAlchemy Base class.
2. A Data transfer Object extends SqlAlchemy Base class.

### UoW (Unit of Work)

TBD

## Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Poetry](https://python-poetry.org/)
* [Docker](https://www.docker.com/)

## How to work

1. Clone and open this repostiroy using VSCode
2. Run Remote-Container 
3. Run `make dev` on the Docker container terminal
4. Access http://127.0.0.1:8000/docs