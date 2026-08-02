from marshmallow import Schema, fields


class RescueSchema(Schema):

    animal_id = fields.Int(required=True)

    latitude = fields.Float(required=True)

    longitude = fields.Float(required=True)

    address = fields.Str(required=True)

    priority = fields.Str(required=True)

    notes = fields.Str()