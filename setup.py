from setuptools import setup, find_packages

setup(
    name='nimble_iot_bc',
    version='1.5',
    description='NIMBLE Platform: IoT and Blockchain based Product Tracking and Tracing Solution',
    url='https://github.com/shantanoo-desai/tracking-iot-blockchain-service',
    author='Shantanoo Desai',
    keywords='rest restful api flask swagger openapi flask-restplus nimble-platform',

    packages=find_packages(),
    install_requires=[
        'flask-restplus==0.13.0',
        'Flask-InfluxDB==0.2',
        'Flask-PyMongo==2.3.0',
        'pymongo==3.9.0',
        'uWSGI==2.0.17.1'
    ],
    include_package_data=True,
    zip_safe=False
)
