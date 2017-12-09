# VERSIONING HELPER FOR MY PROJECTS

The goal of this class is to provide an easy way to implement version changes when building an application using cx_Freeze / Inno Setup.
All you need in the most basic situation is a version file in the root of your project directory.
get_version(self, root="../", file="VERSION.txt", prompt=True) 

# Installation

Download the package from github.
cd <where you put version_hunter package>
Run this command in the terminal:

<pre><code>
python setup.py install

# Or for development use:

python setup.py develop
</code></pre>

#Examples

####Using a typical project structure as below:

Project/
|-- build_scripts/
|   |-- cx_freeze_script
|
|-- project/
|   |-- tests/
|   |   |-- __init__.py
|   |   |-- test_main.py
|   |   
|   |-- __init__.py
|   |-- main.py
|
|-- VERSION.txt
|-- setup.py
|-- README.md

### The simplest case
Your version file is named VERSION.txt and it sits in the root of the project (default settings).
The build script is in a subfolder of root and from there the root can be reached by cd ../
This is the default setting for get_version() method.

<pre><code>
from version_hunter import Versioner
v = Versioner()
version = v.get_version() # Returns for example: 1.0.2

# Use it in your setup:
cx_Freeze.setup(
    name='Your App',
    version=version, # This is where it gets added to the exe's attributes
    description='Your application',
    author='John Smith',
    author_email='jsmith@gmail.com',
    options={'build_exe': {'includes': includes,
                           'excludes': excludes,
                           'packages': packages,
                           'include_files': include_files}},
    executables=executables)
</code></pre>


