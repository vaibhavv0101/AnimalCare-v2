from marshmallow import Schema, fields


class NGOSchema(Schema):

    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    registration_number = fields.Str()
    description = fields.Str()