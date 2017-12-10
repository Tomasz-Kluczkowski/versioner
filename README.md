# VERSIONING HELPER FOR MY PROJECTS

The goal of this program is to provide an easy way to implement version changes when building an application using cx_Freeze / Inno Setup.
All you need in the most basic situation is a version file in the root of your project directory.

# Installation

Download the version_hunter package from github.
cd <where you put version_hunter package>
Run this command in the terminal:

<pre><code>
python setup.py install

# Or for development use:

python setup.py develop
</code></pre>

### Main method to obtain version numbers and usage

<pre>
get_version(self, root="../", file="VERSION.txt", prompt=True):
    """Obtains version number from a file.

    Args:
        root (str): Project's root directory for the search (can be
            relative or absolute) Assumption is that build script
            is run from a subfoler of the project's root.
        file (str): File with the version number. Can be just the name
            or relative / absolute path.
        prompt (bool): Check if user interaction should be enabled
            at initial stage of getting version number.

    Returns:
        ver_num (str): Version number.
    """
</pre>
If prompt is set to _False_, get_version() searches for the version file and returns the text in its first line without any user interaction.

If prompt is set to _True_ (default) user will be presented with the version number found in the terminal and asked if it should be used. If user chooses not to use it the script aborts with system exit code 1 interrupting cx_Freeze script before it is able to build the application (which is what we want at that stage).

# Examples

#### Assuming a typical project structure as below:
<pre>
Project/
|-- build_scripts/
|   |-- cx_freeze_build_script.py
|
|-- project/
|   |-- tests/
|   |   |-- __init__.py
|   |   |-- test_file_to_be_converted_to_exe.py
|   |   
|   |-- __init__.py
|   |-- file_to_be_converted_to_exe.py
|
|-- VERSION.txt
|-- setup.py
|-- README.md
</pre>

### The simplest case
Your version file is named VERSION.txt and it sits in the root of the project (default settings).<br>
In VERSION.txt there is only one line of text with the version number (get_version() reads only one line anyway).<br>
The build script is in a subfolder of project's root and from there the root can be reached by cd ../<br>
You run your cx_Freeze build script from the subfolder where it is, not from project's root.
These are the default setting for get_version() method.


### How to implement it in your cx_Freeze script:
Below code assumes the default settings described in "The simplest case".
<pre><code>
from version_hunter import Versioner
v = Versioner()
version = v.get_version() # Returns version number.

# Use it in your cx_Freeze script like this:
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

### Other possibilities for use

The class is quite flexible and allows user to choose a variety of ways to navigate to the version file in the following order:

1. First it checks if the path to the version file is valid and a file exists there.
2. Failing above it will try to join root/file and check if that is a valid version file.
3. After this it will start searching recursively in the project's root folder and subfolders for the version file. 

#### Absolute path to the version file given
This will try to open the file using the path given. 

<pre><code>
from version_hunter import Versioner
v = Versioner()
version = v.get_version(file="~/Dev/My_project/VERSION.txt") # Returns version number.
</code></pre>

#### Paths to project's root and version file name given
This will join the root and file name and see if the file exists. If not it will attempt to find it recursively.

<pre><code>
from version_hunter import Versioner
v = Versioner()
version = v.get_version(root="~/Dev/My_project, file="ver_file.txt") # Returns version number.
</code></pre>

#### Only the version file name given, uses default root="../"
This will search recursively in the project's folder and all subfolders until first instance of the file is found.

<pre><code>
from version_hunter import Versioner
v = Versioner()
version = v.get_version(file="ver_file.txt") # Returns version number.
</code></pre>

### Reporting of missing version files:
If the version file is not found version_hunter reports it to the user raising an exception and aborting the build process.

/home/tomasz_kluczkowski/.virtualenvs/versioner_env/bin/python /home/tomasz_kluczkowski/Dev/versioner/version_hunter/versioner.py
Traceback (most recent call last):
  File "/home/tomasz_kluczkowski/Dev/versioner/version_hunter/versioner.py", line 143, in <module>
    version_num = v.get_version(file="~/Dev/versioner/tst/erer/ver.txt")
  File "/home/tomasz_kluczkowski/Dev/versioner/version_hunter/versioner.py", line 100, in get_version
    "Version file missing, please check parameters / folders.")
ValueError: Version file missing, please check parameters / folders.

Process finished with exit code 1