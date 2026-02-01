from setuptools import setup, find_packages

setup(
    name='twm',
    version='0.1.0',
    description='Terminal Window Management tool for macOS Terminal.app',
    author='TWM Contributors',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'PyObjC>=9.0',
        'pyyaml>=6.0',
        'pydantic>=2.0',
    ],
    entry_points={
        'console_scripts': [
            'twm=twm.cli:main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
