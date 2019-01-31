import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='optimize-image',  
    version='0.1',
    scripts=['optimize.py'] ,
    author="Franco Burga",
    author_email="franco.burga@gmail.com",
    description="A image optimizer utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/francoburga/optimize-image",
    packages=setuptools.find_packages(),
    data_files=[
        ('/opt/optimize-images/vendor/linux/', ['vendor/linux/cjpeg']),
    ],
    install_requires=[
        'Pillow==5.4.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)