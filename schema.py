import datetime as dt
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


def create_person(
    info: Info,
    first_name: str,
    birth_date: dt.date,
    phone_number: str = "",
    last_name: str = "",
    email: str = "",
) -> PersonType:
    person = Person(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        phone_number=phone_number,
        email=email,
    )
    with Session(info.context.engine) as session:
        session.add(person)
        session.commit()
        return PersonType.from_pydantic(person)


def delete_person(info: Info, id: strawberry.ID) -> PersonType:
    with Session(info.context.engine) as session:
        statement = select(Person).where(Person.id == id)
        person_found = session.exec(statement).one()
        return_obj = PersonType.from_pydantic(person_found)
        session.delete(person_found)
        session.commit()
        return return_obj


def edit_person(
    info: Info,
    id: strawberry.ID,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    birth_date: Optional[dt.date] = None,
) -> PersonType:
    with Session(info.context.engine) as session:
        statement = select(Person).where(Person.id == id)
        person = session.exec(statement).one()
        if first_name is not None:
            person.first_name = first_name
        if last_name is not None:
            person.last_name = last_name
        if email is not None:
            person.email = email
        if phone_number is not None:
            person.phone_number = phone_number
        if birth_date is not None:
            person.birth_date = birth_date
        session.add(person)
        session.commit()
        return PersonType.from_pydantic(person)


@strawberry.type
class Query:
    people: list[PersonType] = strawberry.field(resolver=search_people)
    person: PersonType = strawberry.field(resolver=get_person)


@strawberry.type
class Mutation:
    create_person = strawberry.mutation(create_person)
    delete_person = strawberry.mutation(delete_person)
    edit_person = strawberry.mutation(edit_person)


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema, path="/", context_getter=get_graphql_context
)
