# VERSIONING HELPER FOR MY PROJECTS

The goal of this class is to provide an easy way to implement version changes when building a newer version of an application.
It would be nice to be able to store latest version and have an increment system in place but initially all I want to do is to read VERSION.txt file with a version number, ask user if this is the number they want to use for the newest build and go from there further.


# Specification

- input:
    - reads a line containing a version number from VERSION.txt and stores it in a string.
    - asks user if this is the correct version number to be used for the build.

- output:

    - returns string with the version number
    
# Design

Create class Versioner. Default file to store version is: VERSION.txt
Add a search for first VERSION.txt file available. Use os.walk and check each path for VERSION.txt
In case of path given make sure that it is a file os.path.isfile() and just read it.
If nothing given or only project root - use os.walk to find the first path to VERSION.TXT
If path given is just a directory - append VERSION.txt to it and see if it is a file and read it.

### Methods:

- get_version(path=VERSION.txt): interface for other modules, will contact _reader() to get the version number.
    - parameter: path (str), file name (can be whole path), default = VERSION.txt
    - returns: string with the version number
  
- user(): interface for user, allows deciding if version found is correct.
    - parameter: 
    - return: bool, true - proceed, false - quit
    
- _search_file(root, path): private method, searches for a file with the version number using os.walk.
    - parameter: path (str), file name (can be whole path)
    - root (str) project root directory
    - calls user() asking if correct version number found.
    - returns: string with the version number

- _read_file(path): private method, reads first line of the file and returns version number.
    - parameter: path (tr), file name (path to a valid file with the version number) 

