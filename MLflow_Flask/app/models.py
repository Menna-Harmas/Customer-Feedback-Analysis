from app import db

class Review(db.Model):
    __tablename__ = 'review'

    # Assuming your review table contains these fields based on previous context
    Review_ID = db.Column("Review_ID", db.Integer, primary_key=True)  # Primary key for the review
    # product_asin = db.Column("ProductAsin", db.String(50), nullable=False)
    country = db.Column("Country", db.String(50), nullable=True)
    rating_score = db.Column("RatingScore", db.Integer, nullable=True)
    review_title = db.Column("ReviewTitle", db.String(255), nullable=True)
    review_description = db.Column("ReviewDescription", db.Text, nullable=True)
    # review_url = db.Column("ReviewUrl", db.String(255), nullable=True)
    # is_verified = db.Column("IsVerified", db.Boolean, nullable=True)  # Assuming this is a boolean column
    # date = db.Column("Date", db.Date, nullable=True)                   # Assuming this stores the review date
    # variant = db.Column("Variant", db.String(100), nullable=True)

    def __repr__(self):
        return f'<Review  {self.review_title[:20]}...>'
