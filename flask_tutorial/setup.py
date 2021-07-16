from setuptools import setup, find_packages

setup(
    name='flaskr',
    version='1.0.0',
    # What packages + files within to include? Auto-find.
    # For static/templates, need the MANIFEST file
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)