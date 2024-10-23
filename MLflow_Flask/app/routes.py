from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from app import db
import pandas as pd
from app.models import Review
from app.forms import ReviewForm  # Adjusted to use the simple form class
from app.data_loader import load_data, load_review_data  # Import the load_data function


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve form data
        form = ReviewForm()

        # Create a new Customer instance
        new_review = Review(
                # Review_ID =  form.review_id,
                rating_score=form.rating_score,
                review_title=form.review_title,
                review_description=form.review_description,
                country=form.country,
            )
        db.session.add(new_review)  # Add to session
        db.session.commit()  # Commit the session to save changes
        return redirect(url_for('main.home'))  # Redirect to home after adding

    return render_template('home.html')  # Render home template

@main.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from JSON request body
        data = request.get_json()

        # Convert the incoming data to a DataFrame (as expected by the model)
        df = pd.DataFrame([data])

        # Make prediction using the loaded model from the Flask app context
        prediction = current_app.model.predict(df)
        result = int(prediction[0])  # Convert to integer for JSON response

        # Return the prediction as a JSON response
        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@main.route('/api/review-data', methods=['GET'])
def get_review_data():
    review_data = load_review_data()  # Your data-loading function
    print(review_data) # Your
    return jsonify(review_data.to_dict(orient='records'))


# @main.route('/load_data')
# def load_data_route():
#     customers_df, orders_df, order_items_df, products_df, suppliers_df = load_data()
#     # Here, you can do something with the DataFrames, like pass them to a template or process them further.
#     return "Data loaded successfully!"  # or render a template


@main.route('/dataframes')
def display_dataframes():
    # Query all reviews from the database
    reviews = Review.query.all()

    # Convert the list of reviews to a pandas DataFrame
    # print(reviews)
    review_data = {
        # 'Review ID': [review.id for review in reviews],
        'Rating Score': [review.rating_score for review in reviews],
        'Review Title': [review.review_title for review in reviews],
        'Review Description': [review.review_description for review in reviews],
        'Country': [review.country for review in reviews],
    }
    review_df = pd.DataFrame(review_data)

    # Convert the DataFrame to an HTML table
    review_html = review_df.to_html(classes='table table-striped', index=False)

    # Render the template and pass the table HTML to it
    return render_template('dataframes.html', review_table=review_html)
