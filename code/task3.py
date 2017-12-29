"""
Класс-обертка, реализующий загрузку данных, тренировку, и сохранение и загрузку ранее обученной модели,
а также использование модели для предсказаний. Используется сервером в task4.py.
"""
import pandas as pd
import os
from catboost import CatBoostRegressor
from sqlalchemy import create_engine


class G3Regressor:
        def __init__(self):
            self.data = None
            self.reg = None

        # load training data from database
        def load_data(self, user='test', passwd='12345', db_name='test_db'):
            if self.data is not None:
                print('Data have been already loaded')
            else:
                connect_str = 'mysql+mysqlconnector://{}:{}@localhost/{}'.format(user, passwd, db_name)
                try:
                    engine = create_engine(connect_str)
                    df_mat = pd.read_sql_table('student_mat', engine, index_col='index')
                    df_por = pd.read_sql_table('student_por', engine, index_col='index')
                    df = pd.concat([df_mat, df_por])
                    cols = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob',
                            'reason', 'nursery', 'internet']
                    df.drop_duplicates(cols, inplace=True)
                    self.data = df
                    print('Data loaded successfully')
                except Exception as e:
                    raise e

        # preprocess training / test data
        def preprocess_data(self, df):
            binary_map = {'yes': 1, 'no': 0}
            school_map = {'MS': 0, 'GP': 1}
            sex_map = {'M': 0, 'F': 1}
            address_map = {'R': 0, 'U': 1}
            famsize_map = {'LE3': 0, 'GT3': 1}
            pstatus_map = {'A': 0, 'T': 1}
            job_map = {'services': 0,
                       'health': 1,
                       'other': 2,
                       'at_home': 3,
                       'teacher': 4}
            reason_map = {'course': 0,
                          'other': 1,
                          'reputation': 2,
                          'home': 3}
            guardian_map = {'other': 0, 'father': 1, 'mother': 2}

            df['schoolsup'] = df['schoolsup'].map(binary_map)
            df['famsup'] = df['famsup'].map(binary_map)
            df['paid'] = df['paid'].map(binary_map)
            df['activities'] = df['activities'].map(binary_map)
            df['nursery'] = df['nursery'].map(binary_map)
            df['higher'] = df['higher'].map(binary_map)
            df['internet'] = df['internet'].map(binary_map)
            df['romantic'] = df['romantic'].map(binary_map)
            df['school'] = df['school'].map(school_map)
            df['sex'] = df['sex'].map(sex_map)
            df['address'] = df['address'].map(address_map)
            df['famsize'] = df['famsize'].map(famsize_map)
            df['Pstatus'] = df['Pstatus'].map(pstatus_map)
            df['Mjob'] = df['Mjob'].map(job_map)
            df['Fjob'] = df['Fjob'].map(job_map)
            df['reason'] = df['reason'].map(reason_map)
            df['guardian'] = df['guardian'].map(guardian_map)
            return df

        def train(self):
            if self.data is None:
                self.load_data()
            df = self.data
            target = df['G3']
            df.drop(['G1', 'G2', 'G3'], axis=1, inplace=True)
            train_df = self.preprocess_data(df)
            params = {
                'logging_level': 'Silent',
                'depth': 5,
                'iterations': 1500,
                'l2_leaf_reg': 5,
                'learning_rate': 0.01,
                'random_seed': 12017952
            }
            reg = CatBoostRegressor(**params)
            reg.fit(train_df, target)
            reg.save_model('model.cbm')
            self.reg = reg
            print('Model trained and saved successfully')

        def predict(self, df):
            if self.reg is None:
                if os.path.exists('model.cbm'):
                    self.reg = CatBoostRegressor().load_model('model.cbm')
                    print('Model loaded successfully')
                else:
                    self.train()
            test_df = self.preprocess_data(df)
            preds = self.reg.predict(test_df)
            return preds






