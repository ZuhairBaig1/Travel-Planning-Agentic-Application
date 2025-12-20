from setuptools import find_packages,setup
from typing import List 

def get_requirements()->List[str]:
    # this function returns a clean list of requirements

    requirement_list:List[str]=[]

    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirement.txt file not found.")

    return requirement_list
print(get_requirements())

setup(

    # this defines metadata

    name="AI-travel-planner",
    version='0.0.1',
    author='zuhair',
    author_email='zuhair.md.baig@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)