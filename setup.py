from setuptools import find_packages, setup


setup(
    name="project_contract",
    version="0.0.1",
    description="Project contract management app for ERPNext",
    author="Jie Howe",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
