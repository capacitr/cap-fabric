from distutils.core import setup

setup(
    name='FabricCapacitr',
    version='0.1.0',
    author='patrick aubin',
    author_email='patrick@capacitr.com',
    packages=['fab_capacitr'],
    description='Fab functions used in project fabfiles.',
    install_requires=[
        "fabric",
    ],
)
