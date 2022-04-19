from typing import Optional

import strawberry
from sqlalchemy import extract
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


def search_people(
    info: Info,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    birth_year: Optional[int] = None,
    birth_month: Optional[int] = None,
):
    engine: Engine = info.context.engine
    with Session(engine) as session:
        statement = select(Person)
        if email:
            statement = statement.filter(Person.email.ilike(f"{email}%"))
        if first_name:
            statement = statement.filter(
                Person.first_name.ilike(f"{first_name}%")
            )
        if last_name:
            statement = statement.filter(
                Person.last_name.ilike(f"{last_name}%")
            )
        if birth_year:
            statement = statement.filter(
                extract("year", Person.birth_date) == birth_year
            )
        if birth_month:
            statement = statement.filter(
                extract("month", Person.birth_date) == birth_month
            )
        results = session.exec(statement)
        return list(results)


def get_person(info: Info, id: strawberry.ID) -> Optional[PersonType]:
    with Session(info.context.engine) as session:
        statement = select(Person).where(Person.id == id)
        return session.exec(statement).first()


@strawberry.type
class Query:
    people: list[PersonType] = strawberry.field(resolver=search_people)
    person: PersonType = strawberry.field(resolver=get_person)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(
    schema, path="/", context_getter=get_graphql_context
)
