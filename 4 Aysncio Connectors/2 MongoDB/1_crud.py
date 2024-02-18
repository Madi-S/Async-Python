import os
import asyncio

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


def get_client():
    return AsyncIOMotorClient(os.getenv('MONGO_URL'))


def get_db():
    return get_client().MetaClass


def get_user_collection():
    return get_db().user


async def insert_user() -> ObjectId:
    document = {'first_name': 'Rafael', 'last_name': 'Nadal'}
    result = await get_user_collection().insert_one(document)
    return result.inserted_id


async def find_user_by_id(user_id: ObjectId) -> dict | None:
    document = await get_user_collection().find_one({'_id': user_id})
    return document


async def update_by_id(user_id: ObjectId) -> int:
    result = await get_user_collection().update_one({'_id': user_id}, {'$set': {'is_active': True}})
    return result.modified_count


async def delete_by_id(user_id: ObjectId) -> int:
    result = await get_user_collection().delete_one({'_id': user_id})
    return result.deleted_count


async def main():
    user_id = await insert_user()
    print(f'Inserted user: {user_id}')

    user = await find_user_by_id(user_id)
    print(f'Found user by id: {user}')

    res = await update_by_id(user_id)
    print(f'Updated by id: {res}')

    user = await find_user_by_id(user_id)
    print(f'User after update: {user}')

    res = await delete_by_id(user_id)
    print(f'Delete by id: {res}')

    user = await find_user_by_id(user_id)
    print(f'User after delete: {user}')


if __name__ == '__main__':
    asyncio.run(main())
