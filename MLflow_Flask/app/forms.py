from flask import request

from flask import request

class ReviewForm:
    def __init__(self):
        # self.product_asin = request.form.get('product_asin')
        self.country = request.form.get('country')
        self.rating_score = request.form.get('rating_score')
        self.review_title = request.form.get('review_title')
        self.review_description = request.form.get('review_description')
        # self.review_url = request.form.get('review_url')
        # self.is_verified = request.form.get('is_verified')  # Will return 'on' if checked in the form
        # self.date = request.form.get('date')                # Should be a date field in the form
        # self.variant = request.form.get('variant')
        # self.review_id = request.form.get('Review_ID')
    def __repr__(self):
        return f"<ReviewForm product_asin='{self.product_asin}', review_title='{self.review_title[:20]}...'>"

