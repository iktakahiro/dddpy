# Python DDD & Onion-Architecture Example and Techniques

[![A workflow to run test](https://github.com/iktakahiro/dddpy/actions/workflows/test.yml/badge.svg)](https://github.com/iktakahiro/dddpy/actions/workflows/test.yml)

[English](README.md) | 日本語

**NOTE**: このリポジトリは、「PythonのWebアプリケーションでDDDアーキテクチャを実装する方法」を説明するための例です。参考として使用する場合は、本番環境にデプロイする前に認証とセキュリティの実装を追加してください！

* ブログ投稿: [Python DDD オニオンアーキテクチャ](https://iktakahiro.dev/python-ddd-onion-architecture)

## 技術スタック

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
  * [SQLite](https://www.sqlite.org/index.html)
* [uv](https://github.com/astral-sh/uv)
* [Docker](https://www.docker.com/)

## プロジェクトのセットアップ

1. uvを使用して依存関係をインストールします：

```bash
make install
```

2. Webアプリケーションを実行します：

```bash
make dev
```

## コードアーキテクチャ

ディレクトリ構造は[オニオンアーキテクチャ](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)に基づいています：

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

### ドメイン層

ドメイン層には、コアとなるビジネスロジックとルールが含まれています。以下が含まれます：

1. エンティティ
2. 値オブジェクト
3. リポジトリインターフェース

このプロジェクトでの各コンポーネントの実装方法は以下の通りです：

#### 1. エンティティ

エンティティは一意の識別子を持つドメインモデルです。このプロジェクトでは、`Todo`クラスがエンティティとして実装されています：

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
```

エンティティの主な特徴：

* 一意の識別子（`id`）を持つ
* 状態を変更できる（`update_title`、`start`、`complete`などのメソッド）
* 識別子によって同一性が決定される（`__eq__`メソッドの実装）

#### 2. 値オブジェクト

値オブジェクトは識別子を持たない不変のドメインモデルです。このプロジェクトでは、いくつかの値オブジェクトを実装しています：

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

値オブジェクトの主な特徴：

* `@dataclass(frozen=True)`による不変性の保証
* 値の検証ロジックを含む（`__post_init__`）
* 識別子を持たない
* 値の内容によって同一性が決定される

#### 3. リポジトリインターフェース

リポジトリはエンティティの永続化を担当する抽象化レイヤーです。このプロジェクトでは`TodoRepository`インターフェースを実装しています：

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

リポジトリの主な特徴：

* エンティティの永続化を抽象化
* ドメイン層とインフラ層の境界を定義
* インフラ層で具象実装を提供

### インフラ層

インフラ層はドメイン層で定義されたインターフェースを実装します。以下が含まれます：

1. データベース設定
2. リポジトリの実装
3. 外部サービスとの統合
4. 依存性注入（DI）の設定

### ユースケース層

ユースケース層には、アプリケーション固有のビジネスルールが含まれています。以下が含まれます：

1. ユースケースの実装
2. DTO（データ転送オブジェクト）
3. サービスインターフェース

このプロジェクトでは、1つのユースケースが1つのパブリックメソッドを持つというルールを採用し、各ユースケースを単一の`execute`メソッドを持つ別々のクラスとして実装しています。実装例は以下の通りです：

#### 1. ユースケースインターフェースと実装

各ユースケースは以下の構造に従います：

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

ユースケースの主な特徴：

* ユースケースごとに1つのクラス
* 単一責任の原則
* 明確なインターフェース定義
* コンストラクタによる依存性注入
* インスタンス化のためのファクトリ関数

#### 2. エラーハンドリング

ユースケースはドメイン固有のエラーを処理します：

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

エラーハンドリングの主な特徴：

* ドメイン固有の例外
* 明確なエラー条件
* 状態変更前の検証
* アトミックな操作

### プレゼンテーション層

プレゼンテーション層はHTTPリクエストとレスポンスを処理します。以下が含まれます：

1. FastAPIルートハンドラ
2. リクエスト/レスポンスモデル
3. 入力検証

ハンドラは`presentation/api`ディレクトリの下に配置され、アプリケーションのAPI層を表します。各ドメイン（例：`todo`）は独自のハンドラ、スキーマ、エラーメッセージ定義を持っています。

## 動作方法

1. VSCodeでこのリポジトリをクローンして開きます。
2. リモートコンテナを実行します。
3. Dockerコンテナのターミナルで`make dev`を実行します。
4. APIドキュメントにアクセスします：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

![OpenAPI Doc](./screenshots/openapi_doc.png)

### RESTful APIのサンプルリクエスト

* 新しいTodoを作成する：

```bash
curl --location --request POST 'localhost:8000/todos' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Implement DDD architecture",
    "description": "Create a sample application using DDD principles"
}'
```

* POSTリクエストのレスポンス：

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

* Todoを取得する：

```bash
curl --location --request GET 'localhost:8000/todos'
```

* GETリクエストのレスポンス：

```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Implement DDD architecture",
        "description": "Create a sample application using DDD principles",
        "status": "not_started",
        "created_at": 1614006055213,
        "updated_at": 1614006055213
    }
]
```

## 開発

### テストの実行

```bash
make test
```

### コード品質

このプロジェクトでは、コード品質を維持するために以下のツールを使用しています：

* [mypy](http://mypy-lang.org/) - 静的型チェック
* [ruff](https://github.com/astral-sh/ruff) - リンティング
* [pytest](https://docs.pytest.org/) - テスト

### Docker開発

このプロジェクトには、Dockerベースの開発用の`.devcontainer`設定が含まれています。これにより、異なるマシン間で一貫した開発環境を確保できます。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
