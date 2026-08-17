from extensions import db
from models.announcement import Announcement

class AnnouncementService:
    @staticmethod
    def list_all():
        return [item.to_dict() for item in Announcement.query.order_by(Announcement.published_at.desc()).all()]

    @staticmethod
    def get(item_id):
        return db.session.get(Announcement, item_id)

    @staticmethod
    def create(data):
        item = Announcement(title=data["title"], message=data["message"], category=data.get("category", "Geral"))
        db.session.add(item); db.session.commit()
        return item.to_dict()

    @staticmethod
    def update(item_id, data):
        item = AnnouncementService.get(item_id)
        if not item: return None
        for field in ("title", "message", "category"):
            if field in data: setattr(item, field, data[field])
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete(item_id):
        item = AnnouncementService.get(item_id)
        if not item: return False
        db.session.delete(item); db.session.commit()
        return True
