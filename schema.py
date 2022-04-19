import strawberry  # type: ignore[import]


@strawberry.type
class Book:
    title: str
    author: str


def get_books():
    return [Book(title="The Great Gatsby", author="F. Scott Fitzgerald")]


@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(query=Query)
