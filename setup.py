from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(

    name='typyn',
    version='1.0.8',
    packages=find_packages(where='typyn'),
	package_data={
        'typyn': [
            'typyn/data/*',
            'typyn/resources/*',
            'typyn/user_data/*',
            'typyn/config.toml'
        ]},
    include_package_data=True,
    description='A terminal-based typing game built in Python',
    long_description=long_description,  
    long_description_content_type='text/markdown',
    author='Santiago Fernández',
    author_email='santifernandezok1@gmail.com',
    url='https://github.com/san-fernandez/typy',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
    ],

    install_requires=[
        'typer',
        'windows-curses',
        'toml',
        'pyfiglet',
        'asciichartpy',
        'asciimatics',
    ],

    entry_points={
        'console_scripts': [
            'typyn = typyn.main:app',
            'typyn-run = typyn.main:run',
            'typyn-show-languages = typyn.main:show_languages',
            'typyn-delete-saves = typyn.main:delete_saves',
            'typyn-help = typyn.main:help',
            'typyn-version = typyn.main:version'
        ],
    },

)