import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from settings import settings
from api import Query, Mutation


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)  # , graphiql=False)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


def run():
    uvicorn.run('server:app', reload=True, host=settings.SERVER_HOST, port=settings.SERVER_PORT)