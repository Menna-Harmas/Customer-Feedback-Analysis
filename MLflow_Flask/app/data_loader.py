import pandas as pd
import pyodbc

class Config:
    # Using the connection string that worked for you
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc:///?odbc_connect='
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-JR84GBKF\SQLEXPRESS;'
        'DATABASE=master;'
        'Trusted_Connection=yes;'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Load review data from CSV (adjust the path as necessary)
review_data = pd.read_csv("app/iphone final.csv")
review_df = review_data[:4]  # Adjust the slice as necessary

def load_review_data():
    print("Review data loaded")
    print(review_df.head())  # Print the first few rows to check
    return review_df

# Function to establish the database connection
def get_connection():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-JR84GBKF\SQLEXPRESS;'
        'DATABASE=master;'
        'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

# Function to load data from SQL database
def load_data():
    conn = None
    try:
        # Establish the connection
        conn = get_connection()

        # Define your queries
        country_query = "SELECT * FROM country"
        ratingScore_query = "SELECT * FROM ratingScore"
        reviewTitle_query = "SELECT * FROM reviewTitle"
        reviewDescription_query = "SELECT * FROM reviewDescription"
        
        # Fetch data as pandas DataFrames
        country_df = pd.read_sql(country_query, conn)
        ratingScore_df = pd.read_sql(ratingScore_query, conn)
        reviewTitle_df = pd.read_sql(reviewTitle_query, conn)
        reviewDescription_df = pd.read_sql(reviewDescription_query, conn)

        # Print DataFrame shapes to confirm data was loaded
        print("Country DataFrame shape:", country_df.shape)
        print("RatingScore DataFrame shape:", ratingScore_df.shape)
        print("ReviewTitle DataFrame shape:", reviewTitle_df.shape)
        print("ReviewDescription DataFrame shape:", reviewDescription_df.shape)

        # Rename columns if necessary (adjust column names to match your DB schema)
        country_df.rename(columns={"Id": "countryId"}, inplace=True)
        ratingScore_df.rename(columns={"Id": "ratingScoreId"}, inplace=True)
        reviewTitle_df.rename(columns={"Id": "reviewTitleId"}, inplace=True)
        reviewDescription_df.rename(columns={"Id": "reviewDescriptionId"}, inplace=True)

        # Merge DataFrames (adjust according to your schema)
        Order_Customer_df = pd.merge(reviewTitle_df, reviewDescription_df, on='reviewTitleId', how='inner')
        Order_Customer_Item_df = pd.merge(Order_Customer_df, ratingScore_df, on='ratingScoreId', how='inner')

        # Print previews before slicing
        print("Country DataFrame preview:")
        print(country_df.head())
        print("RatingScore DataFrame preview:")
        print(ratingScore_df.head())
        print("ReviewTitle DataFrame preview:")
        print(reviewTitle_df.head())
        print("ReviewDescription DataFrame preview:")
        print(reviewDescription_df.head())

        # Slice DataFrames if needed
        country_df = country_df[:4]
        ratingScore_df = ratingScore_df[:4]
        reviewTitle_df = reviewTitle_df[:4]
        reviewDescription_df = reviewDescription_df[:4]

        # Print success message
        print("Success: DataFrames loaded successfully.")

        # Return the DataFrames
        return review_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None # Return a tuple of None in case of an error

    finally:
        # Close the connection if it was established
        if conn is not None:
            conn.close()

# Example of calling the functions
if __name__ == "__main__":
    load_review_data()
    review_df = load_data()

    if None in (review_df):
        print("Data could not be loaded correctly.")
    else:
        print("Data loaded successfully and ready for further processing.")
