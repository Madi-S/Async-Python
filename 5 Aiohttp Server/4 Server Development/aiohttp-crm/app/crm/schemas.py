from marshmallow import Schema, fields

from app.web.schemas import OkResponseSchema


class UserSchema(Schema):
    email = fields.Str(required=True)


class UserGetSchema(Schema):
    id = fields.UUID(required=True)


class ListUsersSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


class ListUsersResponseSchema(OkResponseSchema):
    data = fields.Nested(ListUsersSchema)
