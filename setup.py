from distutils.core import setup

setup(
    name='symbios',
    packages=['symbios', 'middlewares'],
    version='1.1.0',
    license='MIT',
    description='A simple asynchronous AMQP library writed for Python.',
    author='Arthuchaut',
    author_email='arthuchaut@gmail.com',
    url='https://github.com/Arthuchaut/symbios',
    download_url='https://github.com/Arthuchaut/symbios/archive/v1.1.0-dev.tar.gz',
    keywords=['Rabbitmq', 'Python', 'Async', 'Broker', 'AMQP'],
    install_requires=['aiormq'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
