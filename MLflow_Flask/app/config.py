import os
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
