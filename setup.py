# Necessary to supress on error in Python 2.7.3 at the completion of
# python setup.py test.
# See http://bugs.python.org/issue15881#msg170215
import multiprocessing        # NOQA

from setuptools.command.test import test as TestCommand
import distutils.command.clean
import os
import setuptools
import sys
import subprocess


class CleanCommand(distutils.command.clean.clean):
    def run(self):
        subprocess.call('find . -name *.pyc -delete'.split(' '))
        subprocess.call('find . -name *.egg -prune -exec rm -rf {} ;'.split(' '))
        subprocess.call('rm -rf build/ dist/ PyLCP.egg-info/ .coverage .noseids'.split(' '))
        distutils.command.clean.clean.run(self)


class NoseTestCommand(TestCommand):
    # Cleaner way to run nose tests using 'python setup.py test'
    # See: http://fgimian.github.io/blog/2014/04/27/running-nose-tests-with-plugins-using-the-python-setuptools-test-command/  # NOQA

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        return_code = subprocess.call('flake8')
        if return_code > 0:
            sys.exit(return_code)

        import nose
        nose.run_exit(argv=['nosetests'])


def read_file(file_name):
    """Utility function to read a file."""
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


def read_first_line(file_name):
    """Read the first line from the specified file."""
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.readline().strip()


setuptools.setup(name='PyLCP',
                 version=read_first_line('version_number.txt'),
                 description="Python client library for Points Loyalty Commerce Platform.",
                 long_description=read_file('README.md'),
                 classifiers=[
                      'Development Status :: 5 - Production/Stable',
                      'Environment :: Web Environment',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: BSD License',
                      'Natural Language :: English',
                      'Operating System :: POSIX :: Linux',
                      'Programming Language :: Python',
                      'Programming Language :: Python :: 2.7',
                      'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                      'Topic :: Software Development :: Libraries :: Python Modules'
                 ],
                 keywords='LCP REST',
                 author='Points International',
                 author_email='',
                 url='',
                 license='',
                 packages=setuptools.find_packages(exclude=['tests']),
                 include_package_data=True,
                 zip_safe=False,
                 install_requires=[
                     'requests',
                     'simplejson',
                 ],
                 entry_points="""
                 # -*- Entry points: -*-
                 """,
                 tests_require=[
                     'coverage',
                     'flake8',
                     'mock',
                     'nose',
                 ],
                 cmdclass={
                     'clean': CleanCommand,
                     'test': NoseTestCommand,
                 },
                 )
