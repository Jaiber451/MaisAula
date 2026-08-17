from sqlalchemy import text
from extensions import db

class ActivityRepository:
    @staticmethod
    def filtered(subject_id=None, status=None, search=None, sort="due_date", direction="asc"):
        # A procedure recebe os filtros; a validação de sort/direction impede injeção por identificadores.
        allowed_sort = {"due_date", "title", "subject_name"}
        sort = sort if sort in allowed_sort else "due_date"
        direction = "DESC" if str(direction).lower() == "desc" else "ASC"

        result = db.session.execute(
            text("CALL sp_list_activities_filtered(:subject_id, :status, :search, :sort_column, :sort_direction)"),
            {
                "subject_id": subject_id,
                "status": status,
                "search": search,
                "sort_column": sort,
                "sort_direction": direction,
            },
        )

        return [dict(row) for row in result.mappings().all()]
