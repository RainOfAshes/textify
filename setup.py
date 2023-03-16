import nltk
from setuptools import setup, find_packages

nltk.download('stopwords')

setup(
    name='textify',
    version='0.0.1',
    packages=find_packages(),
    description='simple text processing API',
    install_requires=[
        'nltk',
        'PyArabic',
        'num2words',
        'pyyaml',
        'joblib',
        'fastapi',
        'uvicorn',
        'pydantic'
    ]
)
