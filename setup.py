from setuptools import setup

setup(
    name='fib',
    version='0.1',
    py_modules=['fib'],
    install_requires=[
        'Click',
        'zenlog',
    ],
    entry_points='''
        [console_scripts]
        fib=fib:cli
    ''',
)
