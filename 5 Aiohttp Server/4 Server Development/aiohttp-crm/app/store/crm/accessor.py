import typing

from app.crm.models import User


if typing.TYPE_CHECKING:
    from app.web.app import Application


class CrmAccessor():
    def __init__(self):
        self.app: 'Application' | None = None

    async def connect(self, app: 'Application'):
        self.app = app

        try:
            self.app.database['users']
        except KeyError:
            self.app.database['users'] = []

        print('Connected to database successfully')

    async def disconnect(self, app: 'Application'):
        self.app = None
        print('Disconnected from database')

    async def add_user(self, user: User):
        self.app.database['users'].append(user)

    async def list_users(self) -> list[User]:
        return self.app.database['users']

    async def get_user(self, _id) -> User | None:
        for user in self.app.database['users']:
            if user._id == _id:
                return user
