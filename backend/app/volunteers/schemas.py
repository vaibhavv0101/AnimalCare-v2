from marshmallow import Schema, fields


class VolunteerSchema(Schema):

    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    skills = fields.Str()
    availability = fields.Str()