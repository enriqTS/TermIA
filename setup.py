from setuptools import setup, find_packages

setup(
    name="termia",
    version="1.0.0",
    description="TermIA - Terminal Inteligente com suporte a IA",
    author="Seu Nome",
    author_email="seu.email@example.com",
    url="https://github.com/seu-usuario/termia",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ply>=3.11",
        "openai>=1.3.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "colorama>=0.4.6",
        "prompt_toolkit>=3.0.39",
    ],
    entry_points={
        "console_scripts": [
            "termia=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)