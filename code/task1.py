import pandas as pd
import os
import argparse
from sqlalchemy import create_engine

parser = argparse.ArgumentParser()
parser.add_argument('--root_dir', dest='ROOT_DIR', default='..')
parser.add_argument('--data_loc', dest='DATA_LOC', default='data')
parser.add_argument('--user', dest='user', default='root')
parser.add_argument('--passwd', dest='passwd', default='12345')
parser.add_argument('--db_name', dest='db_name', default='test_db')
args = parser.parse_args()

ROOT_DIR = args.ROOT_DIR
DATA_DIR = os.path.join(ROOT_DIR, args.DATA_LOC)

# load data to DataFrames
df_mat = pd.read_csv(os.path.join(DATA_DIR, 'student-mat.csv'), sep=';')
df_por = pd.read_csv(os.path.join(DATA_DIR, 'student-por.csv'), sep=';')

# engine for mysql
connect_str = 'mysql+mysqlconnector://{}:{}@localhost'.format(args.user, args.passwd)
engine = create_engine(connect_str)
# creates database & user 'test' with password '12345'
engine.execute('CREATE DATABASE {};'.format(args.db_name))
engine.execute('CREATE USER \'test\'@\'localhost\' IDENTIFIED BY \'12345\';')
engine.execute('GRANT ALL ON {}.* TO \'test\'@\'localhost\''.format(args.db_name))
# connect to created database
connect_str = 'mysql+mysqlconnector://test:12345@localhost/{}'.format(args.db_name)
engine = create_engine(connect_str)
# load data to tables in db
df_mat.to_sql('student_mat', engine)
df_por.to_sql('student_por', engine)