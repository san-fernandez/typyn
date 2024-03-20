from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(

    name='typy',
    version='1.0.0',
    packages=find_packages(),
    description='A terminal-based typing game built in Python',
    long_description=long_description,  
    long_description_content_type='text/markdown',  # Indica que la descripción larga está en formato Markdown
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
            'typy = main:app',
            'typy-run = main:run',
            'typy-show-languages = main:show_languages',
            'typy-delete-saves = main:delete_saves',
            'typy-help = main:help',
            'typy-version = main:version'
        ],
    },

)