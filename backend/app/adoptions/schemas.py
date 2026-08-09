from marshmallow import Schema, fields


class AdoptionSchema(Schema):

    animal_id = fields.Int(required=True)
    reason = fields.Str(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    occupation = fields.Str(required=True)