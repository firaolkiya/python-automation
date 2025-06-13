from setuptools import setup, find_packages

setup(
    name="ticketlink_booking_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "undetected-chromedriver",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "ticketlink_bot=main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight automation tool for Ticketlink booking",
    keywords="ticketlink, booking, automation",
    url="https://github.com/yourusername/ticketlink_booking_bot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 