from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='Population Analyser',
    version='1.0',
    description='Population Analyser',
    license="",
    long_description=long_description,
    author='Maxwell Icharia',
    author_email='maxwellicharia@gmail.com',
    url="https://potraq.herokuapp.com/",
    packages=['Poptraq'],
    include_package_data=True,
    install_requires=[
        'alembic',
        'autoenv',
        'click',
        'dominate',
        'Flask',
        'Flask-Bootstrap',
        'Flask-CLI',
        'Flask-Migrate',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'gunicorn',
        'itsdangerous',
        'Jinja2',
        'Mako',
        'MarkupSafe',
        'postgres',
        'psycopg2',
        'psycopg2-binary',
        'python-dateutil',
        'python-dotenv',
        'python-editor',
        'six',
        'SQLAlchemy',
        'visitor',
        'Werkzeug',
        'WTForms'
        ,
    ],
)
