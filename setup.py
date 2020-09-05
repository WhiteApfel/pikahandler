from setuptools import setup
from io import open


def read(filename):
	with open(filename, encoding='utf-8') as file:
		return file.read()


setup(
	name='pikahandler',
	version='0.0a1',
	packages=['pikahandler'],
	url='https://github.com/whiteapfel/pikahandler',
	license='Mozilla Public License 2.0',
	author='WhiteApfel',
	author_email='white@pfel.ru',
	description='lalala',
	project_urls={
		"Документальное чтиво": "https://pikahandler.readthedocs.io/ru/latest/",
		"Донатик": "https://rocketbank.ru/whiteapfel",
		"Исходнички": "https://github.com/WhiteApfel/pikahandler",
		"Тележка для вопросов": "https://t.me/apfel"
	},
	install_requires=['pika'],
	long_description=read('README.md'),
	long_description_content_type="text/markdown",
	keywords='pika rabbitmq queue handler',
)
