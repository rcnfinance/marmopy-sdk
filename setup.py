from setuptools import find_packages, setup


setup(
    name='marmopy',
    
    version="0.3.0",
    
    description='Marmo wallet Python SDK',
    
    author='Agustin Aguilar, Joaquin Gonzalez, Majed Takieddine',
    
    author_email='agusxrun@gmail.com, jpgonzalezra@gmail.com, majd_takialddin@hotmail.com',
    
    url='https://github.com/ripio/marmopy-sdk',
    
    packages=find_packages(exclude=('tests',)),

    install_requires=[
        "web3==3.16.5",
        "rlp==0.6.0",
        "pycryptodome==3.7.2",
        "coincurve==11.0.0",
        "requests"
    ],

    extras_require={
        "dev": [
            "pylint",
            "pytest",
            "tox>=1.8.0"
        ]
    },

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    
)