from setuptools import setup

package_name = 'pub_sub'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abdelrahman',
    maintainer_email='abdelrahman@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = pub_sub.publisher:main',
            'listener = pub_sub.subscriber:main',
        'composed = pub_sub.pubsub:main'
        ],
    },
)
