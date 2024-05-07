from setuptools import setup

setup(
    name='illustris_python_zoom',
    version='1.0.0',
    packages=["illustris_python_zoom"],
    install_requires=["numpy", "h5py", "six"],
    tests_require=["nose","coverage"],
)
