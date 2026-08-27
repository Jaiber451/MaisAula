from models.user import User
from services.helpers import ensure_fields
class UserCreateService:
    def __init__(self, data): self.data=data or {}
    def execute(self):
        ensure_fields(self.data, ['nome', 'email'])
        return User.salvar(self.data).to_dict()
