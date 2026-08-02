from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    full_name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100)
    )

    email = fields.Email(required=True)

    phone = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=15)
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=8)
    )

    role = fields.Str(required=True)
    
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)