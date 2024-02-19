import bson
import typing
from dataclasses import field
from marshmallow import Schema, ValidationError, fields, missing
from marshmallow_dataclass import dataclass


class ObjectIdField(fields.Field):
    def _deserialize(
        self,
        value: typing.Any,
        attrs: str | None,
        data: typing.Mapping[str | None] | None,
        **kwargs
    ):
        try:
            return bson.ObjectId(value)
        except Exception:
            raise ValidationError(f'Invalid ObjectId {value}')

    def _serialize(self, value: typing.Any, attr: str, obj: typing.Any, **kwargs):
        if value is None:
            return missing
        return str(value)


Schema.TYPE_MAPPING[bson.ObjectId] = ObjectIdField


@dataclass
class User:
    first_name: str
    last_name: str
    is_active: bool
    _id: bson.ObjectId | None = field(default=None)

    Schema: typing.ClassVar[typing.Type[Schema]] = Schema
