from models.user import User
class UserUpdateService:
    def __init__(self, item_id, data): self.item_id=item_id; self.data=data or {}
    def execute(self):
        item=User.buscar_por_id(self.item_id)
        return item.atualizar(self.data).to_dict() if item else None
