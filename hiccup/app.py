import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL

from hiccup import SETTINGS
from hiccup.graphql import Query, Mutation, get_context

# GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation, config=StrawberryConfig(
    disable_field_suggestions=not SETTINGS.debug_enabled,
))
graphql_app = GraphQLRouter(
    schema,
    debug=SETTINGS.debug_enabled,
    context_getter=get_context,
    subscription_protocols=[
        GRAPHQL_TRANSPORT_WS_PROTOCOL,
        GRAPHQL_WS_PROTOCOL,
    ],
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
