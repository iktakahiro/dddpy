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

1. 仮想環境を作成して有効化します：
```bash
python -m venv .venv
source .venv/bin/activate  # Unix/macOS
# または
.venv\Scripts\activate  # Windows
```

2. uv を使用して依存関係をインストールします：
```bash
uv sync
```

## コードアーキテクチャ

ディレクトリ構造は[オニオンアーキテクチャ](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)に基づいています：

```
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

### エンティティ

Pythonでエンティティを表現するには、オブジェクトの同一性を確保するために `__eq__()` メソッドを使用します。

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

### 値オブジェクト

値オブジェクトを表現するには、`@dataclass` デコレーターを `eq=True` および `frozen=True` と共に使用します。

以下のコードは、値オブジェクトとしての本のISBNコードを実装しています。

* [isbn.py](./dddpy/domain/book/isbn.py)

```python
@dataclass(init=False, eq=True, frozen=True)
class Isbn:
    value: str

    def __init__(self, value: str):
        if not validate_isbn(value):
            raise ValueError("Value should be a valid ISBN format.")
        object.__setattr__(self, "value", value)
```

### DTO (データ転送オブジェクト)

DTO (データ転送オブジェクト)は、ドメインオブジェクトをインフラ層から分離するための良い実践です。

最小のMVCアーキテクチャでは、モデルはORM（オブジェクト関係マッピング）によって提供されるベースクラスを継承することがよくあります。しかし、その場合、ドメイン層が外部層に依存することになります。

この問題を解決するために、2つのルールを設定できます：

1. ドメイン層のクラス（エンティティや値オブジェクトなど）は、SQLAlchemyのBaseクラスを継承しない。
2. データ転送オブジェクトは、ORMクラスを継承する。
   * [book_dto.py](./dddpy/infrastructure/sqlite/book/book_dto.py)

### CQRS

CQRS（コマンドとクエリの責任分離）パターンは、読み取り操作と書き込み操作を分離するために有用です。

1. **ユースケース層**にリードモデルとライトモデルを定義します：
   * [book_query_model.py](./dddpy/usecase/book/book_query_model.py)
   * [book_command_model.py](./dddpy/usecase/book/book_command_model.py)

2. クエリ：
   * **ユースケース層**にクエリサービスインターフェースを定義します：
     * [book_query_service.py (interface)](./dddpy/usecase/book/book_query_service.py)
   * **インフラ層**にクエリサービスの実装を定義します：
     * [book_query_service.py](./dddpy/infrastructure/sqlite/book/book_query_service.py)

3. コマンド：
   * **ドメイン層**にリポジトリインターフェースを定義します：
     * [book_repository.py (interface)](./dddpy/domain/book/book_repository.py)
   * **インフラ層**にリポジトリの実装を定義します：
     * [book_repository.py](./dddpy/infrastructure/sqlite/book/book_repository.py)

4. ユースケース：
   * ユースケースはリポジトリインターフェースまたはクエリサービスインターフェースに依存します：
     * [book_query_usecase.py](./dddpy/usecase/book/book_query_usecase.py)
     * [book_command_usecase.py](./dddpy/usecase/book/book_command_usecase.py)
   * ユースケースは、リードモデルまたはライトモデルのインスタンスをメインルーチンに返します。

### UoW (ユニット・オブ・ワーク)

ドメイン層の分離に成功しても、トランザクション管理の方法などの問題が残ります。

UoW（ユニット・オブ・ワーク）パターンが解決策となりえます。

まず、ユースケース層に基づいたUoWパターンのインターフェースを定義します。`begin()`, `commit()`, `rollback()`メソッドはトランザクション管理に関連します。

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

次に、上記のインターフェースを使用してインフラ層にクラスを実装します。

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

`session`プロパティはSQLAlchemyのセッションです。

## 動作方法

1. このリポジトリをクローンしてVSCodeで開きます。
2. リモートコンテナを実行します。
3. Dockerコンテナのターミナルで `make dev` を実行します。
4. APIドキュメントにアクセスします： [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

![OpenAPI Doc](./screenshots/openapi_doc.png)

### RESTful APIのサンプルリクエスト

* 新しい本を作成する：

```bash
curl --location --request POST 'localhost:8000/books' \
--header 'Content-Type: application/json' \
--data-raw '{
    "isbn": "978-0321125217",
    "title": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
    "page": 560
}'
```

* POSTリクエストのレスポンス：

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

* 本を取得する：

```bash
curl --location --request GET 'localhost:8000/books'
```

* GETリクエストのレスポンス：

```json
[
    {
        "id": "e74R3Prx8SfcY8KJFkGVf3",
        "
