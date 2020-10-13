from setuptools import setup

with open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="bakapi",
    version="0.2",
    url="https://github.com/mvolfik/bakapi",
    project_urls={
        "Documentation": "https://github.com/mvolfik/bakapi/blob/master/README.md",
        "Code": "https://github.com/mvolfik/bakapi",
        "Issue tracker": "https://github.com/mvolfik/bakapi/issues",
    },
    license="MIT License",
    author="Matěj Volf",
    author_email="mat.volfik@gmail.com",
    description="Bakaláři API v3 client",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Czech",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
    ],
    py_modules=["bakapi"],
    install_requires=["requests"],
)
