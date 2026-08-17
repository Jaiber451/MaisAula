from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db
from controllers.student_controller import student_bp
from controllers.teacher_controller import teacher_bp
from controllers.subject_controller import subject_bp
from controllers.class_controller import class_bp
from controllers.activity_controller import activity_bp
from controllers.announcement_controller import announcement_bp
from controllers.dashboard_controller import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(student_bp, url_prefix="/api/students")
    app.register_blueprint(teacher_bp, url_prefix="/api/teachers")
    app.register_blueprint(subject_bp, url_prefix="/api/subjects")
    app.register_blueprint(class_bp, url_prefix="/api/classes")
    app.register_blueprint(activity_bp, url_prefix="/api/activities")
    app.register_blueprint(announcement_bp, url_prefix="/api/announcements")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "+Aula API"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Rota não encontrada"}), 404

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({"error": "Erro interno do servidor"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
