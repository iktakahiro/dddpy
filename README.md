# Python DDD example using FastAPI

*NOTE: This repository is an example to explain 'how to implement DDD architecture on Python web applicaiton'. If you will to use this as a reference, add your implementation of authentication and security before deploying to the real world!!*

## Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
  * [SQLite](https://www.sqlite.org/index.html)
* [Poetry](https://python-poetry.org/)
* [Docker](https://www.docker.com/)

## Code Architecture

For this implementation, I've adopted the [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/).

Directory structure:

```tree
├── main.py
├── dddpy
│   ├── domain
│   │   └── book
│   │       ├── book.py  # Entiry
│   │       ├── book_exception.py  # Exception definitions
│   │       ├── book_repository.py  # Repository interface
│   │       └── isbn.py
│   ├── infrastructure
│   │   └── sqlite
│   │       ├── book
│   │       │   ├── book_dto.py  # DTO using SQLAlchemy
│   │       │   ├── book_query_service.py  # Query service implementation
│   │       │   └── book_repository.py  # Repository implementation
│   │       └── database.py
│   ├── presentation
│   │   └── schema
│   │       └── book
│   │           └── book_error_message.py
│   └── usecase
│       └── book
│           ├── book_command_model.py  # Write models including schemas of the RESTFul API
│           ├── book_command_usecase.py
│           ├── book_query_model.py   # Read models including schemas
│           ├── book_query_service.py  # Query service interface
│           └── book_query_usecase.py
└── tests
```

### Entity

To represent an Entity in Python, use `__eq__()` method to ensure the identity of the object.

```python
class Book:
    def __init__(self, id: str, title: str):
        self.id: str = id
        self.title: str = title

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Book):
            return self.id == o.id

        return False
```

### Value Object

To represent a Value Object, use `@dataclass` decorator with `eq=True` and `frozen=True`.

The following code implements the ISBN code of a book as a Value Object.

```python
@dataclass(init=False, eq=True, frozen=True)
class Isbn:
    value: str

    def __init__(self, value: str):
        if value is None:
            raise ValueError("value is required.")
        if !validate_isbn(value):
            raise ValueError("value should be valid ISBN format.")

        object.__setattr__(self, "value", value)
```

### DTO (Data Transfer Object)

DTO (Data Transfer Object) is a good practice to isolate domain objects from the infrastructuer layer.

On a minimum MVC architecture, models often inherit a base class provided by a O/R Mappaer. But in that case, the domain layer would be dependent on the outer layer. The same can be said for Python applications using SQLAlchemy.

To solve this problem, we can simply set two rules:

1. A Domain layer classes (such as an Entity or a Value Object) **DO NOT** extend SQLAlchemy Base class.
2. A Data transfer Objects extend the O/R mapper class.

### CQRS

TBD

### UoW (Unit of Work)

Even if we succeed in isolating the domain layer, some issues remains. One of them is how to manage transactions.

UoW (Unit of Work) Pattern can be the solution.

TBD

## How to work

1. Clone and open this repostiroy using VSCode
2. Run Remote-Container
3. Run `make dev` on the Docker container terminal
4. Access the API document http://127.0.0.1:8000/docs

![OpenAPI Doc](./screenshots/openapi_doc.png)

### Sample requests for the RESTFul API

* Create a new book:

```bash
curl --location --request POST 'localhost:8000/books' \
--header 'Content-Type: application/json' \
--data-raw '{
    "isbn": "978-0321125217",
    "title": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
    "page": 560
}'
```

* Response of the POST request:

```json
{
    "id": "HH9uqNdYbjScdiLgaTApcS",
    "isbn": "978-0321125217",
    "title": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
    "page": 560,
    "read_page": 0,
    "created_at": 1614007224642,
    "updated_at": 1614007224642
}
```

* Get books:

```bash
curl --location --request GET 'localhost:8000/books'
```

* Response of the GET request:

```json
[
    {
        "id": "e74R3Prx8SfcY8KJFkGVf3",
        "isbn": "978-0321125217",
        "title": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
        "page": 560,
        "read_page": 0,
        "created_at": 1614006055213,
        "updated_at": 1614006055213
    }
]
```
