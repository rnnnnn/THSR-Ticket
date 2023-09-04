from setuptools import setup, find_packages

try:
    with open("requirements.txt", "r") as in_file:
        requirements = in_file.readlines()
except FileNotFoundError:
    print("Error: requirements.txt file not found.")
    requirements = []

setup(
    name='thsr-ticket',
    version='0.2',
    description='An automatic booking program for Taiwan High Speed Railway(THSR).',
    author='Raito',
    author_email='info.raito.site@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={'console_scripts': ['thsr-ticket = thsr_ticket.main:main']}
)
