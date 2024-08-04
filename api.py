from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry

app = FastAPI()

# Define your GraphQL schema


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str = "stranger") -> str:
        return f"Hello, {name}!"


schema = strawberry.Schema(query=Query)

# Create a GraphQLRouter and include it in your FastAPI app
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# To run the server, use: uvicorn app:app --reload
