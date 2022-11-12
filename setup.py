from setuptools import setup, find_namespace_packages

setup(name='ContactBook',
      version='1.0',
      description='bot assistant',
      url='https://github.com/Laplas00/ContactBook',
      author='Bogdan Gaidarzhy, Mykola Prystash, Vasiliy Hlushchenko, Daniil Zubov',
      author_email='flyingcircus@example.com, msprystash@gmail.com, Gluschenkov88@gmail.com, danielzubov12@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': [
          'ContactBook = ContactBook.main:main']}
      )
