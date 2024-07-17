from setuptools import setup, find_packages

setup(
    name="hero-journey-writer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langgraph",
        "langchain",
        "langchain_openai",
        "python-dotenv",
    ],
)
