# -*- coding: utf-8 -*-
import os
import yaml

os.environ['WORKING_DIRECTORY'] = '/Users/jeongmoonwon/Downloads/Courses/BKMS1/team_project/book_recsys'
os.environ['LOGGING_DIRECTORY'] = '/Users/jeongmoonwon/Downloads/Courses/BKMS1/team_project/book_recsys/logs'
WORKING_DIRECTORY = os.environ['WORKING_DIRECTORY']
LOGGING_DIRECTORY = os.environ['LOGGING_DIRECTORY']

conf = False

yaml_path = os.path.join(WORKING_DIRECTORY, 'resources/config_prd.yaml')

with open(yaml_path) as file:
    conf = yaml.safe_load(file)
