import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'humanoid_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ola',
    maintainer_email='ola@todo.todo',
    description='Humanoid robot package',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ball_tracker_node = humanoid_robot.ball_tracker_node:main',
            'serial_bridge = humanoid_robot.serial_bridge:main',
            'ball_detector = humanoid_robot.ball_detector:main',
            'camera_node = humanoid_robot.camera_node:main',
        ],
    },
)
