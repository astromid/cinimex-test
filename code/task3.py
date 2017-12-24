import numpy as np
import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://test:12345@localhost/test_db')
df_mat = pd.read_sql_table('student_mat', engine, index_col='index')
df_por = pd.read_sql_table('student_por', engine, index_col='index')
df = pd.concat([df_mat, df_por])
cols = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob',
        'reason', 'nursery', 'internet']
df.drop_duplicates(cols, inplace=True)