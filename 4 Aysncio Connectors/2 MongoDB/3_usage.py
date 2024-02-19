import os
import asyncio
from bson import ObjectId
from dataclasses import asdict
from motor.motor_asyncio import AsyncIOMotorClient

from .schema import User
# from `.2_schema` import User


def get_client():
    return AsyncIOMotorClient(os.getenv('MONGO_URL'))


def get_db():
    return get_client().metaclass


def get_user_collection():
    return get_db().user


async def insert_user(user: User) -> ObjectId:
    document = asdict(user)
    del document['_id']
    result = await get_user_collection().insert_one(document)
    return result.inserted_id


async def find_user_by_id(user_id: ObjectId) -> User | None:
    document = await get_user_collection().find_one({'_id': user_id})
    if not document:
        return None
    return User.Schema().load(document)


async def run():
    user_id = await insert_user(
    User(first_name='Alexander', last_name='Opryshko', is_tutor=True)
    )
    print('insert_user', user_id)
    user = await find_user_by_id(user_id)
    print('find_user_by_id', user)


if __name__ == '__main__':
    asyncio.run(run())
