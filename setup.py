
import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

required = [
	"Django>=1.6",
	"django-bootstrap-form>=3.1",
	"django-haystack",
	]

setup(
	name="Farnsworth",
	version="1.1.0",
	author="Karandeep Nagra",
	url="https://github.com/knagra/farnsworth",
	author_email="karandeepsnagra@gmail.com",
	packages=find_packages(),
	include_package_data=True,
	description="Website for BSC houses.",
	long_description=README,
	install_requires=required +  ["elasticsearch>=1.0.0"],
	tests_require=required,
	test_suite="runtests.runtests",
	package_data={
		"": ["*/static/*/*/*", "*/templates/*", "templates/search/*/*/*"],
		},
	classifiers=[
		"Environment :: Web Environment",
		"Framework :: Django",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		],
	dependency_links=[
		"git://github.com/toastdriven/django-haystack.git#egg=django_haystack-master",
		],
	extras_require={
		"PostgreSQL": ["psycopg2"],
		"social-auth": ["python-social-auth"],
		},
	)