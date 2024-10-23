import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import json
import warnings
from sklearn.exceptions import ConvergenceWarning
from flask_sqlalchemy import SQLAlchemy
from models import Review
# from app  # Import your Flask app to access the DB
# from app.models import Review  # Import models here to avoid circular imports

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="mlflow.*")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# Function to set up MLflow experiment
def set_mlflow_experiment(experiment_name):
    mlflow.set_experiment(experiment_name)

# Function to prepare data
def prepare_data(review_data):
    imputer = SimpleImputer(strategy='median')
    encoded_review_data = pd.get_dummies(review_data, drop_first=True)
    
    X = encoded_review_data.drop('ratingScore', axis=1)
    y = encoded_review_data['ratingScore']
    
    X_imputed = imputer.fit_transform(X)
    X_imputed = pd.DataFrame(X_imputed, columns=X.columns)  # Retain feature names
    
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.30, stratify=y, random_state=2022)
    
    return X_train, X_test, y_train, y_test

# Updated feature importance logging
def log_feature_importance(best_model, X_train):
    feature_importance = best_model.coef_[0]
    importance_dict = {feature: coef for feature, coef in zip(X_train.columns, feature_importance)}
    with open("feature_importance.json", "w") as f:
        json.dump(importance_dict, f)
    mlflow.log_artifact("feature_importance.json")

# Train model function
def train_model(X_train, y_train, X_test, y_test):
    with mlflow.start_run():
        param_grid = {'C': [0.1, 1, 10]}
        grid = GridSearchCV(LogisticRegression(multi_class='ovr'), param_grid, cv=5)
        grid.fit(X_train, y_train)
        
        best_model = grid.best_estimator_
        mlflow.log_param("best_C", grid.best_params_['C'])
        
        y_pred = best_model.predict(X_test)
        metrics = classification_report(y_test, y_pred, output_dict=True)
        
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["weighted avg"]["precision"])
        mlflow.log_metric("recall", metrics["weighted avg"]["recall"])
        mlflow.log_metric("f1-score", metrics["weighted avg"]["f1-score"])

        if len(set(y_train)) == 2:
            auc = roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1])
            mlflow.log_metric("roc_auc", auc)
            fpr, tpr, thresholds = roc_curve(y_test, best_model.predict_proba(X_test)[:, 1])
            plt.figure()
            plt.plot(fpr, tpr, color='blue', label='ROC curve (area = %0.2f)' % auc)
            plt.plot([0, 1], [0, 1], color='red', linestyle='--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver Operating Characteristic')
            plt.legend(loc='lower right')
            plt.savefig("roc_curve.png")
            mlflow.log_artifact("roc_curve.png")
        
        log_feature_importance(best_model, X_train)
        
        mlflow.sklearn.log_model(best_model, "model")
        model_uri = "runs:/{}/model".format(mlflow.active_run().info.run_id)
        mlflow.register_model(model_uri, "Product_Review_Rating_Prediction")

        return best_model, metrics

# Updated main function to use reviews from the database
def main_train_model():
    try:
        set_mlflow_experiment("Product Review Rating Prediction")

        # Query the reviews from the database
        reviews = Review.query.all()

        # Convert reviews to a pandas DataFrame
        review_data = {
            'ratingScore': [review.rating_score for review in reviews],
            'reviewTitle': [review.review_title for review in reviews],
            'reviewDescription': [review.review_description for review in reviews],
            'country': [review.country for review in reviews]
        }
        review_df = pd.DataFrame(review_data)

        # Debug print to verify data loading
        print("Loaded review data:", review_df.head())

        X_train, X_test, y_train, y_test = prepare_data(review_df)
        model, metrics = train_model(X_train, y_train, X_test, y_test)

        print("Model training completed successfully.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # with app.app_context():
        main_train_model()









