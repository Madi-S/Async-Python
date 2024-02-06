from marshmallow import Schema,	fields


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


user_data = {
    'name': 'Ken',
    'email': 'ken@yahoo.com',
    'created_at': '2014-08-11T05:26:03.869245',
}
schema = UserSchema()
result = schema.load(user_data)
print(result)
# {'name': 'Ken', 'email': 'ken@yahoo.com', 'created_at': datetime.datetime(2014, 8, 11, 5, 26, 3, 869245)}
