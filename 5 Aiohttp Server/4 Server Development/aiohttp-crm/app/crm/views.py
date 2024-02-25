import uuid

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import docs, request_schema, querystring_schema, response_schema

from app.web.app import View
from app.crm.models import User
from app.web.utils import json_response
from app.web.schemas import OkResponseSchema
from app.crm.schemas import UserSchema, ListUsersResponseSchema


class AddUserView(View):
    @docs(tags=['crm'], summary='Creates a new user')
    @request_schema(UserSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = self.request['data']
        user = User(
            _id=uuid.uuid4(),
            email=data['email']
        )
        await self.request.app.crm_accessor.add_user(user)
        print(self.request.app.database)
        return json_response()


class ListUsersView(View):
    @docs(tags=['crm'], summary='Gets all users')
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [
            {'_id': str(user._id), 'email': user.email}
            for user in users
        ]
        return json_response(raw_users)


class GetUserView(View):
    @docs(tags=['crm'], summary='Get user by given query id')
    async def get(self):
        user_id = self.request.query['id']
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            raw_user = {'user': {'_id': str(user._id), 'email': user.email}}
            return json_response(raw_user)
        return HTTPNotFound
