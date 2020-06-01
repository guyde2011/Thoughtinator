from setuptools import setup, find_packages


setup(
    name = 'thoughtinator',
    version = '1.3.2',
    author = 'Guyde (Guy Chervonits)',
    description = 'A TAU CS project',
    packages = find_packages(),
    install_requires = ['click',
                        'flask',
                        'Flask-Cors'
                        'furl',
                        'matplotlib',
                        'numpy',
                        'peewee',
                        'pika',
                        'protobuf',
                        'Pillow',
                        'psycopg2',
                        'requests',
                        'Werkzeug',
                        'bson',
    ]
    tests_require = ['pytest',
                     'codecov',
    ],
)