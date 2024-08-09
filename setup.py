from setuptools import find_packages, setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(
    name='intro_writer',  # This should match your package directory name
    version="0.0.1",
    description="writer of intros",
    license="MIT",
    author="federicomoreno613",
    author_email="federicomoreno613@gmail.com",
    packages=find_packages(),  # This will find the 'intro_writer' package
    install_requires=requirements,
    test_suite="tests",
    include_package_data=True,
    zip_safe=False
)


