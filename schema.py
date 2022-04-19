import strawberry
from sqlalchemy.engine import Engine
from sqlmodel import Session
from sqlmodel import select
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from dependencies import get_graphql_context
from models import Person


@strawberry.experimental.pydantic.type(model=Person, all_fields=True)
class PersonType:
    pass


@strawberry.type
class Book:
    title: str
    author: str


def get_books():
    return [Book(title="The Great Gatsby", author="F. Scott Fitzgerald")]


def get_people(info: Info):
    engine: Engine = info.context.engine
    with Session(engine) as session:
        statement = select(Person)
        results = session.exec(statement)
        return list(results)


@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)
    people: list[PersonType] = strawberry.field(resolver=get_people)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(
    schema, path="/", context_getter=get_graphql_context
)
