# Python DDD & Onion-Architecture Example and Techniques

[![A workflow to run test](https://github.com/iktakahiro/dddpy/actions/workflows/test.yml/badge.svg)](https://github.com/iktakahiro/dddpy/actions/workflows/test.yml)

English | [日本語](README.ja_JP.md)

**NOTE**: This repository is an example to demonstrate "how to implement DDD architecture in a Python web application." If you use this as a reference, ensure to implement authentication and security before deploying it to a real-world environment!

* My blog post: <https://iktakahiro.dev/python-ddd-onion-architecture>

## Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
  * [SQLite](https://www.sqlite.org/index.html)
* [uv](https://github.com/astral-sh/uv)
* [Docker](https://www.docker.com/)

## Project Setup

1. Install dependencies using uv:

```bash
make install
```

2. Run the web app

```bash
make dev
```

## Code Architecture

The directory structure is based on [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/):

```tree
├── main.py
├── dddpy
│   ├── domain
│   │   └── book
│   ├── infrastructure
│   │   └── sqlite
│   │       ├── book
│   │       └── database.py
│   ├── presentation
│   │   └── schema
│   │       └── book
│   └── usecase
│       └── book
└── tests
```

### Entity

To represent an Entity in Python, use the `__eq__()` method to ensure the object's identity.

* [book.py](./dddpy/domain/book/book.py)

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

To represent a Value Object, use the `@dataclass` decorator with `eq=True` and `frozen=True`.

The following code implements a book's ISBN code as a Value Object.

* [isbn.py](./dddpy/domain/book/isbn.py)

```python
@dataclass(init=False, eq=True, frozen=True)
class Isbn:
    value: str

    def __init__(self, value: str):
        if !validate_isbn(value):
            raise ValueError("Value should be a valid ISBN format.")

        object.__setattr__(self, "value", value)
```

### DTO (Data Transfer Object)

DTO (Data Transfer Object) is a good practice to isolate domain objects from the infrastructure layer.

In a minimal MVC architecture, models often inherit a base class provided by an ORM (Object-Relational Mapper). However, this would make the domain layer dependent on the outer layer.

To solve this problem, we can set two rules:

1. Domain layer classes (such as Entities or Value Objects) **DO NOT** extend the SQLAlchemy Base class.
2. Data Transfer Objects extend the ORM class.
   * [book_dto.py](./dddpy/infrastructure/sqlite/book/book_dto.py)

### CQRS

CQRS (Command and Query Responsibility Segregation) pattern is useful for separating read and write operations.

1. Define read models and write models in the **usecase layer**:
   * [book_query_model.py](./dddpy/usecase/book/book_query_model.py)
   * [book_command_model.py](./dddpy/usecase/book/book_command_model.py)

2. Query:
   * Define query service interfaces in the **usecase layer**:
     * [book_query_service.py (interface)](./dddpy/usecase/book/book_query_service.py)
   * Implement query service implementations in the **infrastructure layer**:
     * [book_query_service.py](./dddpy/infrastructure/sqlite/book/book_query_service.py)

3. Command:
   * Define repository interfaces in the **domain layer**:
     * [book_repository.py (interface)](./dddpy/domain/book/book_repository.py)
   * Implement repository implementations in the **infrastructure layer**:
     * [book_repository.py](./dddpy/infrastructure/sqlite/book/book_repository.py)

4. Usecases:
   * Usecases depend on repository interfaces or query service interfaces:
     * [book_query_usecase.py](./dddpy/usecase/book/book_query_usecase.py)
     * [book_command_usecase.py](./dddpy/usecase/book/book_command_usecase.py)
   * Usecases return an instance of the read or write model to the main routine.

### UoW (Unit of Work)

Even if we succeed in isolating the domain layer, some issues remain. One of them is *how to manage transactions*.

The UoW (Unit of Work) Pattern can be a solution.

First, define an interface based on the UoW pattern in the usecase layer. The `begin()`, `commit()`, and `rollback()` methods manage transactions.

* [book_command_usecase.py](./dddpy/usecase/book/book_command_usecase.py)

```python
class BookCommandUseCaseUnitOfWork(ABC):
    book_repository: BookRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
```

Second, implement a class in the infrastructure layer using the above interface.

* [book_repository.py](./dddpy/infrastructure/sqlite/book/book_repository.py)

```python
class BookCommandUseCaseUnitOfWorkImpl(BookCommandUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        book_repository: BookRepository,
    ):
        self.session: Session = session
        self.book_repository: BookRepository = book_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
```

The `session` property is a SQLAlchemy session.

## How to Work

1. Clone and open this repository using VSCode.
2. Run Remote-Container.
3. Run `make dev` in the Docker container terminal.
4. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

![OpenAPI Doc](./screenshots/openapi_doc.png)

### Sample Requests for the RESTful API

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

This revised documentation clarifies the steps and code involved in setting up a Domain-Driven Design (DDD) architecture using Python. It also provides sample requests to interact with the RESTful API.
