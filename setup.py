import setuptools
import os


def read_requirements(filename=None):
    filepath = os.path.join(os.path.dirname(__file__),
                            filename or 'requirements.txt')
    with open(filepath, 'r') as reader:
        return [line.strip().replace('===', '==')
                for line in reader.readlines()]


setuptools.setup(
    name='Furry Computing Machine',
    version='0.0.1',
    description='A testing project, with a catchy name',
    author='MariaS210',
    author_email='marias210@example.com',
    url='https://github.com/mariaS210/furry-computing-machine',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    classifiers=[
        'Development Status :: 2 - Proof of Concept',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)