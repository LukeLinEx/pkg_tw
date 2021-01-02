from setuptools import setup

setup(
    name='pkg_tw',
    packages=['taiwanese'],
    include_package_data=True,
    install_requires=[
        "flask", "boto3", "pyyaml", "numpy", "pandas", "bson",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "oauth2client"
    ]
)
