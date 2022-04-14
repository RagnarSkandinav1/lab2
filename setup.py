from setuptools import setup
setup(
    name='python_serializers',
    version='0.0.1',
    packages=[
        'cli',
        'serializers',
        'serializers/exception',
        'serializers/json',
        'serializers/pickle',
        'serializers/toml',
        'serializers/yaml',
    ],
    tests_require=[
        'pytest==7.0.1',
        'pytest-cov==3.0.0',
        'coverage==6.3.1',
    ],
    test_suite='tests',
)

