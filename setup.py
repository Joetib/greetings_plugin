
import io
import os
from setuptools import find_packages, setup
from typing import Dict, List

HERE = os.path.abspath(os.path.dirname(__file__))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def load_readme() -> str:
    with io.open(os.path.join(HERE, "README.md"), "rt", encoding="utf8") as f:
        readme = f.read()
    # Replace img src for publication on pypi
    return readme



def load_requirements(*requirements_paths) -> List[str]:
    """
    Load all requirements from the specified requirements files.
    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split("#")[0].strip() for line in open(path).readlines() if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line) -> bool:
    """
    Return True if the requirement line is a package requirement.
    Returns:
        bool: True if the line is not blank, a comment, a URL, or an included file
    """
    return not (
        line == ""
        or line.startswith("-c")
        or line.startswith("-r")
        or line.startswith("#")
        or line.startswith("-e")
        or line.startswith("git+")
    )


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
ABOUT = """GREETINGS
An extension built for ibleducation interview
"""
print("Found packages: {packages}".format(packages=find_packages()))
print("requirements found: {requirements}".format(requirements=load_requirements("requirements.txt")))

setup(
    name="greetings_plugin",
    version="0.1.0",
    packages=find_packages(),
    package_data={"": ["*.html"]},  # include any Mako templates found in this repo.
    include_package_data=True,
    license_files=("LICENSE.txt",),
    license="AGPLv3",
    description="Django plugin to enhance feature set of base Open edX platform.",
    long_description=load_readme(),
    author="Oti Boateng Joseph",
    author_email="otiboatengjoe@gmail.com",
    install_requires=load_requirements("requirements.txt"),
    zip_safe=False,
    keywords="Django, Open edX, Plugin",
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 0.1 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
    ],
    entry_points={
       
        "lms.djangoapp": [
            "openedx_plugin = greetings_plugin.apps:GreetingsConfig",
            
        ],
        "cms.djangoapp": [
            "openedx_plugin_cms = greetings_plugin.apps:CustomPluginCMSConfig",
        ],
    },
    extras_require={
        "Django": ["Django>=3.2"],
    },
)