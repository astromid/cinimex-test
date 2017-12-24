import pandas as pd
import os
from sqlalchemy import create_engine

ROOT_DIR = '..'
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# load data to DataFrames
df_mat = pd.read_csv(os.path.join(DATA_DIR, 'student-mat.csv'), sep=';')
df_por = pd.read_csv(os.path.join(DATA_DIR, 'student-por.csv'), sep=';')

# engine for mysql database
# requires already created database 'test_db' & user 'test' with password '12345'
engine = create_engine('mysql+mysqlconnector://test:12345@localhost/test_db')

# load data to tables in db
df_mat.to_sql('student_mat', engine)
df_por.to_sql('student_por', engine)