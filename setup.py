from setuptools import setup

setup(
    name = 'psunlinked',
    version = '0.1.0',
    descrption = 'List processes running with unlinked executable files',
    author = 'Jonathon Reinhart',
    author_email = 'Jonathon.Reinhart@gmail.com',
    url = 'https://github.com/JonathonReinhart/psunlinked',
    python_requires = '>=3.4.0',
    install_requires = [
        'psutil',           # python3-psutil on Debian
    ],
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
    ],
    py_modules = [
        'psunlinked',
    ], 
    entry_points = dict(
        console_scripts = [
            'psunlinked = psunlinked:main',
        ],
    ),
)
