import os
class Config:
    SQLALCHEMY_DATABASE_URI = ("mssql+pyodbc://Helder:Helder@PC-DEV8/flaskdb?driver=ODBC+Driver+17+for+SQL+Server")
    SQLALCHEMY_TRACK_MODIFICATIONS = False