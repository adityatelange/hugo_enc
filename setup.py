from setuptools import setup


setup(
    name='hugo_encryptor',
    version="1.0",
    packages=["hugo_encryptor"],
    author="Li4n0, adityatelange",
    install_requires=[
        "beautifulsoup4==4.9.3",
        "pycryptodome==3.10.1",
        "lxml==4.6.3"
    ],
    description="A python tool to encrypt hugo posts",
    package_data={'hugo_encryptor': ['decoder_script.js']},
    url='https://github.com/adityatelange/hugo_encryptor',
    entry_points={'console_scripts': [
        'hugo_encryptor = hugo_encryptor:main']},
    classifiers=[
        "Programming Language :: Python",
    ],
)
