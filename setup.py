from setuptools import setup
from setuptools.command.install import install as _install

def _post_install():
    pass

class DHQueryInstall(_install):
    """Custom installer for DHQuery"""
    def run(self):
        _install.run(self)

        self.execute(_post_install, [], msg="Running post install task")

setup(
    # Application name:
    name="dhquery",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Alex Proca",
    author_email="alex.proca@gmail.com",

    # Packages
    packages=["dhquery"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/alexproca/dhquery",

    #
    # license="LICENSE.txt",
    description="Python DHCP testing util",

    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "http://pydhcplib.tuxfamily.org/download/pydhcplib-0.6.2.tar.gz",
        ],
    cmdclass={'install': DHQueryInstall}
    )
