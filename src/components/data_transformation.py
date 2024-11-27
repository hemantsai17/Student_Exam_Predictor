import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utilis import save_object

@dataclass

class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):

        '''
        This function si responsible for data trnasformation
        
        '''

        try:
            num_features = ['writing_score','reading_score']
            cat_features = [
                'gender' , 'race_ethnicity' , 'parental_level_of_education' , 'lunch' , 'test_preparation_course'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ('imputer' , SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer' , SimpleImputer(strategy='most_frequent')),
                    ('One_Hot_Encoding',OneHotEncoder())
                ]
            )

            logging.info(f'numerical features {num_features}')
            logging.info(f'categorical features {cat_features}')

            preprocessor = ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,num_features),
                ("cat_pipelines",cat_pipeline,cat_features)
                ]
            )

            return preprocessor
        
        except Exception as e:
            CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info('Train and Test data imported')

            preprocessor_obj = self.get_data_transformer_object()

            target_column = 'math_score'
            numerical_column = ['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info('Done splitting dataset into independent and dependent columns')
            logging.info('Applying preprocessing to splitted data')
            
            print('------------------------------------------------')
            preprocessed_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            preprocessed_test_arr = preprocessor_obj.transform(input_feature_test_df)

            
            train_arr = np.c_[
                preprocessed_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[preprocessed_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")


            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj= preprocessor_obj

            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            CustomException(e,sys)


# if __name__ == '__main__':
#     obj = DataTransformation()
#     obj.initiate_data_transformation('artifacts\train.csv' ,'artifacts\test.csv' )