## It is responsible for creating ML application as package and can be distributed around

from setuptools import find_packages , setup
from typing import List

HYPHEN_E_DOT = '-e .'
def install_requirements(path:str)->List[str]:
    #This function will return list of requirements from requirements.txt
    req =[]
    with open(path) as file_obj:
        req= file_obj.readlines()
        new_req = [r.replace('\n','') for r in req]
        if HYPHEN_E_DOT in new_req:
            new_req.remove(HYPHEN_E_DOT)
        
    return new_req


setup(
    name='StudentPerformancePredictor',
    version='1.0.0',
    author='Hemant',
    author_email='hemantsai3@gmail.com',
    packages=find_packages(),
    install_reqires =install_requirements('requirements.txt')
)