from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from models import UserModel, TokenModel, UsageModel

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        include_relationships = True
        exclude = ("password",)

    tokens = Nested("TokenSchema", many=True, exclude=("user",), dump_only=True)

class TokenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TokenModel
        load_instance = True
        include_relationships = True
        exclude = ("token",)

    usages = Nested('UsageSchema', many=True, dump_only=True)

class UsageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UsageModel
        load_instance = True
        include_relationships = True