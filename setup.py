from setuptools import setup, find_packages

setup(
    name='pyphone_recorder',
    version='1.0.0',
    url='https://github.com/aussedatlo/pyphone_recorder',
    author='Louis Aussedat',
    author_email='aussedat.louis@gmail.com',
    description='python application to record audio with old phone',
    packages=find_packages(),
        scripts=[
                'bin/pyphone-recorder',
    ],
    install_requires=[
        'yaspin >= 2.2.0',
        'RPi.GPIO >= 0.5.8',
        'pyaudio >= 0.2.11',
        'pyalsaaudio >= 0.9.2'
    ],
)
