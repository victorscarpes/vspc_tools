from setuptools import find_packages, setup, find_packages

setup(name="vspc_tools",
      version="1.0",
      description="Diversas funções que utilizo o tempo inteiro",
      author="Victor Sabiá Pereira Carpes",
      url="https://github.com/victorscarpes/vspc_tools",
      install_requires=["to_precision @ git+https://bitbucket.org/william_rusnack/to-precision.git"],
      packages=find_packages()
      )