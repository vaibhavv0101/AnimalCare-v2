from marshmallow import Schema, fields, validate


class DonationSchema(Schema):

    donor_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    email = fields.Email(
        required=True
    )

    phone = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )

    amount = fields.Decimal(
        required=True,
        as_string=True,
        places=2,
        validate=validate.Range(min=1)
    )

    purpose = fields.String(
        required=True,
        validate=validate.OneOf([
            "Animal Food",
            "Medical Treatment",
            "Emergency Rescue",
            "Shelter Support",
            "Adoption Support",
            "General Animal Care"
        ])
    )

    payment_reference = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=150)
    )

    is_anonymous = fields.Boolean(
        load_default=False
    )