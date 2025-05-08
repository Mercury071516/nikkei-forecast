from setuptools import setup

APP = ['nikkei.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['yfinance', 'selenium'],
    'includes': ['tkinter', 'yfinance', 'selenium'],
    'plist': {
        'CFBundleName': 'Nikkei Forecast',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleIdentifier': 'com.yourname.nikkeiapp',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
