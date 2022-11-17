from setuptools import setup

with open("README.md") as file:
    read_me_description = file.read()

setup(
    name="elastic-search-lib",
    version="0.1.14",
    author="Sergey Listov",
    author_email="slistov@mail.ru",
    description="Elastic search library",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slistov/elastic-search-lib.git",
    packages=['elastic_search_lib'],
    install_requires=[
        'elasticsearch[async]==8.4.3',
        'pytest',
        'pytest-asyncio'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
