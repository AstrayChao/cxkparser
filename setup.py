from setuptools import setup, find_packages
setup(
    name="cxkParser",
    version='0.2.4',
    keywords={"pip", "cxkParser"},
    description="for cxk",
    license="MIT Licence",
    author='dxc',
    author_email='dxclmrl@outlook.com',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["beautifulsoup4", "pandas"],
    entry_points={
        'console_scripts': ['cxkParser=cxkParser.main:main']
    }
)
