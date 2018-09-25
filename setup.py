from setuptools import setup

package_name = 'extended_dummy'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'node'
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Martin Dahl',
    author_email='martin.dahl@gmail.com',
    maintainer='Martin Dahl',
    maintainer_email='martin.dahl@gmail.com',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Examples of minimal publishers using rclpy.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'node = node:main'
        ],
    },
)
