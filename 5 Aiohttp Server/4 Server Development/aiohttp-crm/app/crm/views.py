import uuid

from aiohttp.web_response import json_response
from aiohttp.web_exceptions import HTTPNotFound

from app.web.app import View
from app.crm.models import User


class AddUserView(View):
    async def post(self):
        data = await self.request.json()
        user = User(
            _id=uuid.uuid4(),
            email=data['email']
        )
        await self.request.app.crm_accessor.add_user(user)
        print(self.request.app.database)
        return json_response(data={'status': 'ok'})


class ListUsersView(View):
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [
            {'_id': str(user._id), 'email': user.email}
            for user in users
        ]
        return json_response(data={'status': 'ok', 'users': raw_users})


class GetUserView(View):
    async def get(self):
        user_id = self.request.query['id']
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            raw_user = {'_id': str(user._id), 'email': user.email}
            return json_response(data={'status': 'ok', 'user': raw_user})
        return HTTPNotFound
