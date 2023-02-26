from setuptools import setup

meta = {}
with open('lattehhpel/about.py') as f:
    exec(f.read(), meta)

long_description = open('README.md').read()

setup(
    name=meta['__package__'],
    version=meta['__version__'],
    description=meta['__description__'],
    url=meta['__url__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    license='Propietary',
    platforms='Windows',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=['lattehhpel'],
    package_data={
        'lattehhpel': [
            './tests/*.*'
        ]
    },
    install_requires=[
        # 1st level dependencies
        'pytest==7.1.1',
        'pytest-html==3.1.1',
        'pyserial==3.5',
        # 2nd level dependencies
        'atomicwrites==1.4.0',      # required by pytest
        'attrs==21.4.0',            # required by pytest
        'colorama==0.4.4',          # required by pytest
        'iniconfig==1.1.1',         # required by pytest
        'packaging==21.3',          # required by pytest
        'pluggy==1.0.0',            # required by pytest
        'py==1.11.0',               # required by pytest
        'tomli==2.0.1',             # required by pytest
        'pytest-metadata==2.0.1',   # required by pytest-html
        # 3rd level dependencies
        'pyparsing==3.0.7',         # required by packaging
    ],
    python_requires='>=3.7',
)

print(f'\n==> Package {meta["__package__"]} {meta["__version__"]} generated successfully in ./dist folder')
