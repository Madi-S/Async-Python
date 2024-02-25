import uuid

from aiohttp.web_response import json_response

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
