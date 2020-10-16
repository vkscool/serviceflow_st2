"""ServiceFlow_St2 package setup file"""
import setuptools


setuptools.setup(
    name="ServiceFlow Stackstorm Package",
    description="Contains sensor and actions for ServiceFlow StackStorm",
    url="https://git.source.akamai.com/projects/CST/repos/serviceflow_st2/browse",
    long_description="Contains sensor and actions for ServiceFlow StackStorm",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
)
