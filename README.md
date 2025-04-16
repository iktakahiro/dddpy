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
│   ├── domain
│   │   └── todo
│   │       ├── entities
│   │       │   └── todo.py
│   │       ├── value_objects
│   │       │   ├── todo_title.py
│   │       │   ├── todo_description.py
│   │       │   ├── todo_id.py
│   │       │   └── todo_status.py
│   │       ├── repositories
│   │       │   └── todo_repository.py
│   │       └── exceptions
│   ├── infrastructure
│   │   ├── di
│   │   │   └── injection.py
│   │   └── sqlite
│   │       ├── database.py
│   │       └── todo
│   │           ├── todo_repository.py
│   │           └── todo_dto.py
│   ├── presentation
│   │   └── api
│   │       └── todo
│   │           ├── handlers
│   │           │   └── todo_api_route_handler.py
│   │           ├── schemas
│   │           │   └── todo_schema.py
│   │           └── error_messages
│   │               └── todo_error_message.py
│   └── usecase
│       └── todo
│           ├── create_todo_usecase.py
│           ├── update_todo_usecase.py
│           ├── start_todo_usecase.py
│           ├── find_todos_usecase.py
│           ├── find_todo_by_id_usecase.py
│           ├── complete_todo_usecase.py
│           └── delete_todo_usecase.py
└── tests
```

### Domain Layer

The domain layer contains the core business logic and rules. It includes:

1. Entities
2. Value Objects
3. Repository Interfaces

Here's how each component is implemented in this project:

#### 1. Entities

Entities are domain models with unique identifiers. In this project, the `Todo` class is implemented as an entity:

```python
class Todo:
    def __init__(
        self,
        id: TodoId,
        title: TodoTitle,
        description: Optional[TodoDescription] = None,
        status: TodoStatus = TodoStatus.NOT_STARTED,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        completed_at: Optional[datetime] = None,
    ):
        self._id = id
        self._title = title
        self._description = description
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at
        self._completed_at = completed_at

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Todo):
            return self._id == obj._id
        return False
```

Key characteristics of entities:

* Have a unique identifier (`id`)
* Can change state (methods like `update_title`, `start`, `complete`)
* Identity is determined by the identifier (`__eq__` method implementation)

The `__eq__` method implementation in this project follows DDD principles:

```python
def __eq__(self, obj: object) -> bool:
    if isinstance(obj, Todo):
        return self._id == obj._id
    return False
```

Key points of this implementation:

* Identity is determined solely by the identifier (`id`)
* Type safety is ensured with `isinstance` check
* Clean implementation focusing on the essential characteristic of entities

#### 2. Value Objects

Value objects are immutable domain models without identifiers. This project implements several value objects:

```python
@dataclass(frozen=True)
class TodoTitle:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError('Title is required')
        if len(self.value) > 100:
            raise ValueError('Title must be 100 characters or less')
```

Key characteristics of value objects:

* Immutability guaranteed by `@dataclass(frozen=True)`
* Include value validation logic (`__post_init__`)
* No identifier
* Identity is determined by value content

#### 3. Repository Interfaces

Repositories are abstraction layers responsible for entity persistence. This project implements the `TodoRepository` interface:

```python
class TodoRepository(ABC):
    @abstractmethod
    def save(self, todo: Todo) -> None:
        """Save a Todo"""

    @abstractmethod
    def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        """Find a Todo by ID"""

    @abstractmethod
    def find_all(self) -> List[Todo]:
        """Get all Todos"""

    @abstractmethod
    def delete(self, todo_id: TodoId) -> None:
        """Delete a Todo by ID"""
```

Key characteristics of repositories:

* Abstract entity persistence
* Define boundaries between domain and infrastructure layers
* Concrete implementations provided in the infrastructure layer

### Infrastructure Layer

The infrastructure layer implements the interfaces defined in the domain layer. It includes:

1. Database configurations
2. Repository implementations
3. External service integrations
4. Dependency Injection (DI) setup

#### 1. Repository Implementations

The repository implementation is done as follows:

```python
class TodoRepositoryImpl(TodoRepository):
    """SQLite implementation of Todo repository interface."""

    def __init__(self, session: Session):
        """Initialize repository with SQLAlchemy session."""
        self.session = session

    def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        """Find a Todo by its ID."""
        try:
            row = self.session.query(TodoDTO).filter_by(id=todo_id.value).one()
        except NoResultFound:
            return None

        return row.to_entity()

    def save(self, todo: Todo) -> None:
        """Save a new Todo item."""
        todo_dto = TodoDTO.from_entity(todo)
        try:
            existing_todo = (
                self.session.query(TodoDTO).filter_by(id=todo.id.value).one()
            )
        except NoResultFound:
            self.session.add(todo_dto)

        else:
            existing_todo.title = todo_dto.title
            existing_todo.description = todo_dto.description
            existing_todo.status = todo_dto.status
            existing_todo.updated_at = todo_dto.updated_at
            existing_todo.completed_at = todo_dto.completed_at
```

Unlike the repository interface, the implementation code in the infrastructure layer can contain details specific to a particular technology (SQLite in this example). It's often beneficial to clearly indicate the underlying technology in directory names (e.g., `sqlite`) or class names, rather than strictly adhering to abstract interface definitions.

#### 2. Data Transfer Object

In Onion Architecture, inner layers (like the domain layer) do not depend on outer layers (infrastructure, presentation). Therefore, when exchanging data between layers, object conversion might be necessary to prevent details of one layer (e.g., infrastructure's database model) from leaking into others. Data Transfer Objects (DTOs) fulfill this conversion role.

The following `TodoDTO` class inherits from SQLAlchemy's base class as an O/R Mapper and implements methods for converting to and from domain layer objects:

```python
class TodoDTO(Base):
    """Data Transfer Object for Todo entity in SQLite database."""

    __tablename__ = 'todo'
    id: Mapped[UUID] = mapped_column(primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(index=True, nullable=False)
    created_at: Mapped[int] = mapped_column(index=True, nullable=False)
    updated_at: Mapped[int] = mapped_column(index=True, nullable=False)
    completed_at: Mapped[int] = mapped_column(index=True, nullable=True)

    def to_entity(self) -> Todo:
        """Convert DTO to domain entity."""
        return Todo(
            TodoId(self.id),
            TodoTitle(self.title),
            TodoDescription(self.description),
            TodoStatus(self.status),
            datetime.fromtimestamp(self.created_at / 1000, tz=timezone.utc),
            datetime.fromtimestamp(self.updated_at / 1000, tz=timezone.utc),
            datetime.fromtimestamp(self.completed_at / 1000, tz=timezone.utc)
            if self.completed_at
            else None,
        )

    @staticmethod
    def from_entity(todo: Todo) -> 'TodoDTO':
        """Convert domain entity to DTO."""
        return TodoDTO(
            id=todo.id.value,
            title=todo.title.value,
            description=todo.description.value if todo.description else None,
            status=todo.status.value,
            created_at=int(todo.created_at.timestamp() * 1000),
            updated_at=int(todo.updated_at.timestamp() * 1000),
            completed_at=int(todo.completed_at.timestamp() * 1000)
            if todo.completed_at
            else None,
        )
```

By converting `TodoDTO` objects (dependent on SQLAlchemy) retrieved from the database into the domain layer's `Todo` entity before returning them to the use case layer, we prevent the use case layer from depending on infrastructure layer details. This also maintains consistency with the return type (`Todo` entity) defined in the repository interface.

### Usecase Layer

The usecase layer contains the application-specific business rules. It includes:

1. Usecase implementations
2. Error handling related to use cases

In this project, each use case is implemented as a separate class with a single public `execute` method, following the rule of "one public method per use case". This design ensures clear separation of concerns and makes the code more maintainable. Here's how it's implemented:

#### 1. Use Case Interface and Implementation

Each use case follows this structure:

```python
class CreateTodoUseCase:
    """CreateTodoUseCase defines a use case interface for creating a new Todo."""

    @abstractmethod
    def execute(
        self, title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> Todo:
        """execute creates a new Todo."""


class CreateTodoUseCaseImpl(CreateTodoUseCase):
    """CreateTodoUseCaseImpl implements the use case for creating a new Todo."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(
        self, title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> Todo:
        """execute creates a new Todo."""
        todo = Todo.create(title=title, description=description)
        self.todo_repository.save(todo)
        return todo
```

Key characteristics of use cases:

* One class per use case
* Single responsibility principle
* Clear interface definition
* Dependency injection through constructor
* Factory function for instantiation

#### 2. Error Handling

Use cases handle domain-specific errors:

```python
class StartTodoUseCaseImpl(StartTodoUseCase):
    def execute(self, todo_id: TodoId) -> None:
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        if todo.is_completed:
            raise TodoAlreadyCompletedError

        if todo.status == TodoStatus.IN_PROGRESS:
            raise TodoAlreadyStartedError

        todo.start()
        self.todo_repository.save(todo)
```

Key characteristics of error handling:

* Domain-specific exceptions
* Clear error conditions
* Validation before state changes
* Atomic operations

### Presentation Layer

The presentation layer handles HTTP requests and responses. It includes:

1. FastAPI route handlers
2. Request/Response models
3. Input validation

The handlers are organized under the `presentation/api` directory, which represents the API layer of the application. Each domain (like `todo`) has its own controller, schema, and error message definitions.

## How to Work

1. Clone and open this repository using VSCode.
2. Run Remote-Container.
3. Run `make dev` in the Docker container terminal.
4. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

![OpenAPI Doc](./screenshots/openapi_doc.png)

### Sample Requests for the RESTful API

* Create a new todo:

```bash
curl --location --request POST 'localhost:8000/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Implement DDD architecture",
    "description": "Create a sample application using DDD principles"
}'
```

* Response of the POST request:

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Implement DDD architecture",
    "description": "Create a sample application using DDD principles",
    "status": "TODO",
    "created_at": 1614007224642,
    "updated_at": 1614007224642
}
```

* Get todos:

```bash
curl --location --request GET 'localhost:8000/todos'
```

* Response of the GET request:

```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Implement DDD architecture",
        "description": "Create a sample application using DDD principles",
        "status": "not_started",
        "created_at": 1614007224642,
        "updated_at": 1614007224642
    }
]
```

## Development

### Running Tests

```bash
make test
```

### Code Quality

This project uses several tools to maintain code quality:

* [mypy](http://mypy-lang.org/) for static type checking
* [ruff](https://github.com/astral-sh/ruff) for linting
* [pytest](https://docs.pytest.org/) for testing

### Docker Development

The project includes a `.devcontainer` configuration for Docker-based development. This ensures a consistent development environment across different machines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
