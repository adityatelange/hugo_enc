from setuptools import setup


setup(
    name='hugo_enc',
    version="1.0",
    packages=["hugo_enc"],
    author="Li4n0, adityatelange",
    install_requires=[
        "beautifulsoup4==4.9.3",
        "pycryptodome==3.10.1",
        "lxml==4.6.3"
    ],
    description="A python tool to encrypt hugo posts",
    package_data={'hugo_enc': ['decoder_script.js']},
    url='https://github.com/adityatelange/hugo_enc',
    entry_points={'console_scripts': [
        'hugo_enc = hugo_enc:main']},
    classifiers=[
        "Programming Language :: Python",
    ],
)
