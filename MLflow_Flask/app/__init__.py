from flask import Flask
from flask_sqlalchemy import SQLAlchemy   
import mlflow      

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')  # Specify the template folder
    app.config.from_object('app.config.Config')  # Load configuration from Config class
    app.model = mlflow.sklearn.load_model("models:/Product_Review_Rating_Prediction/1")

    db.init_app(app)  # Initialize the SQLAlchemy instance with the app

    with app.app_context():
        from app.models import Review  # Import models here to avoid circular imports
        db.create_all()  # Create database tables

    from app.routes import main  # Import routes
    app.register_blueprint(main)  # Register the blueprint

    return app
