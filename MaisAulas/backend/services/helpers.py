from sqlalchemy.exc import IntegrityError
def ensure_fields(data, fields):
    missing=[f for f in fields if data.get(f) in (None,"")]
    if missing: raise ValueError("Campos obrigatórios: " + ", ".join(missing))
def commit_error(exc):
    if isinstance(exc, IntegrityError): return "Não foi possível concluir a operação por causa de um relacionamento ou dado duplicado."
    return "Não foi possível concluir a operação."
