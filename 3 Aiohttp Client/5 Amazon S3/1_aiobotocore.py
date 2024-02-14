import asyncio
from aiobotocore.session import get_session


AWS_ACCESS_KEY_ID = '1234'
AWS_SECRET_ACCESS_KEY = '4321'


async def go():
    bucket = 'dataintake'
    filename = 'dummy.bin'
    folder = 'aiobotocore'
    key = f'{folder}/{filename}'

    session = get_session()
    async with session.create_client(
        's3',
        region_name='us-west-2',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    ) as client:
        # Upload object to Amazon S3
        data = b'\x01' * 1024
        r = await client.put_object(Bucket=bucket, Key=key, Body=data)
        print(r)

        # Download S3 Object properties of file we just uploaded
        r = await client.get_object_acl(Bucket=bucket, Key=key)
        print(r)

        # This ensures that the connection is correctly re-used/closed
        async with r['Body'] as stream:
            assert await stream.read() == data

        # List S3 Objects using paginator
        paginator = client.get_paginator('list_objects')
        async for result in paginator.paginate(
            Bucket=bucket, Prefix=folder
        ):
            for content in result.get('Contents', []):
                print(content)

        # Delete object from S3
        r = await client.delete_object(Bucket=bucket, Key=key)
        print(r)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())
