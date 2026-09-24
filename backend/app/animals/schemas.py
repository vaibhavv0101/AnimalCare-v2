from marshmallow import Schema, fields


class AnimalSchema(Schema):

    name = fields.Str(required=True)

    species = fields.Str(required=True)

    breed = fields.Str(allow_none=True)

    gender = fields.Str(allow_none=True)

    age = fields.Int(allow_none=True)

    color = fields.Str(allow_none=True)

    weight = fields.Float(allow_none=True)

    rescue_location = fields.Str(allow_none=True)

    health_status = fields.Str(allow_none=True)

    vaccination_status = fields.Str(allow_none=True)

    description = fields.Str(allow_none=True)

    adoption_status = fields.Str()