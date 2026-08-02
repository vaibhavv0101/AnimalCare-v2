from marshmallow import Schema, fields


class AnimalSchema(Schema):

    name = fields.Str(required=True)

    species = fields.Str(required=True)

    breed = fields.Str()

    gender = fields.Str()

    age = fields.Int()

    color = fields.Str()

    weight = fields.Float()

    rescue_location = fields.Str()

    health_status = fields.Str()

    vaccination_status = fields.Str()

    description = fields.Str()