import asyncio
import csv
from faker import Faker


fake = Faker()


async def request_users_data(uid: int) -> dict:
    await asyncio.sleep(0.5)
    return {'id': uid, 'name': fake.name(), 'email': fake.email()}


ids = [i for i in range(1, 11)]

loop = asyncio.get_event_loop()

with open('out.csv', 'w') as fh:
    fieldnames = ['id', 'name', 'email']
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    for uid in ids:
        writer.writerow(loop.run_until_complete(request_users_data(uid)))
