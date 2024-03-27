from marshmallow import Schema, fields, validate

class UsageSchema(Schema):
    usage_id = fields.Int(dump_only=True)
    token_id = fields.Int(required=True, load_only=True)
    endpoint = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)
    request_size = fields.Int(required=True)
    response_size = fields.Int(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class TokenSchema(Schema):
    token_id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    token = fields.Str(required=True, load_only=True)
    expiration = fields.DateTime(required=True)
    usages = fields.List(fields.Nested(UsageSchema), dump_only=True)

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
    tokens = fields.List(fields.Nested(TokenSchema), dump_only=True)
