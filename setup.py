from distutils.core import setup

setup(
    name='pydantic_openapi',
    version='0.1.0',
    packages=['src'],
    url='',
    license='GNU',
    author='Yury Blagoveshchenskiy',
    author_email='yurathestorm@gmail.com',
    description='Generate OpenAPI schema from pydantic models',
    install_requires=['pydantic'],
    entry_points={
        'console_scripts': ['oapigen=src.command_line:main'],
    }
)
