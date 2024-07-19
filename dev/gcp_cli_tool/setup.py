from setuptools import setup, find_packages

setup(
    name='gcp_cli_tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Dependencies are listed in requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'gcp-cli = gcp_cli_tool.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
