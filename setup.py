from setuptools import find_packages, setup


setup(
    name='marmopy',
    version="0.1.0",
    description='Marmo wallet Python SDK',
    author='Majed Takieddine',
    author_email='majd_takialddin@hotmail.com',
    python_requires='>=3.6,<4',
    url='https://github.com/ripio/marmopy-sdk',
    packages=find_packages(exclude=('tests',)),
    install_requires=["web3>=4.8.2"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    
)