![Xeekworx](http://xeekworx.com/images/github/xeekworx_logo.png)
Autoversion
===========

**Autoversion is a command-line tool written in Python that looks for preprocessor definitions in a C/C++ header file and modifies the value to increment version values.**

Note: Python 2.7+ is needs to be installed on the system that uses this utility.

HOW IT WORKS
------------

As an example, if you give it the definition name *MYAPP_VERSION*, it will search (line by line) the header file for this *#define* and increment any version values it detects. Multiple definition names can be given.

The format of the version should be, X.X.X.X, but each part is optional (so X.X is valid or even just X). Also the value separator can be a period or a comma and quotes (as for strings) is also fine. Below is an example of how autoversion interprets your version values:

    MAJOR.MINOR.REVISION.BUILD or 1.16.52.1

The version is incremented in this way ...

 1. **MAJOR**: This is not incremented unless it is the only value that exists in the version. If this is the only value in the version, it is incremented by + 1.
 2. **MINOR**: This is set to the two digit representation of the current year.
 3. **REVISION**: This is the month and day combined. If the current local date is May 2, the revision will be set to 52.
 4. **BUILD**: This is incremented by + 1.

The version value separator, leading and trailing quotations, and trailing "\0" will be maintained when the version is modified.

COMMAND LINE
------------
> **usage:** autoversion.py [--help] FILE [MACRO [MACRO ...]]
> 
> autoversion
> 
> **positional arguments:**
> *FILE* Source file to modify (required)
> *MACRO* Macros to modify (1 or more required)
> 
> **optional arguments:**   --help, -?

CONFIGURING VISUAL STUDIO (C/C++)
-----------------------------------
You can configure your Visual Studio project to run autoversion every time the project is built by following these instructions. Note that these instructions are assuming that your project is a C/C++ one, other language projects could have very different configuration windows.

 1. Right click on your project and select "Properties" or press ALT + ENTER with the project selected.
 2. Make sure the *Configuration* dropdown is set to "All Configurations" and that *Platform* is set to "All Platforms".
 3. On the left side select *Configuration Properties > Build Events > Pre-Build Event*.
 4. For the Command Line "autoversion.py "myversion.h MYDEF_PRODUCTVERSION"
 5. Make sure you put in the path for autoversion.py if it's not in the project's directory. Also make sure that you put in the path/filename of your header and the name of your #define in place of mine. Multiple definition arguments are possible.

![Visual Studio Screen Shot](http://xeekworx.com/images/github/autoversion/autoversion_screenshot.png)

> Written with [StackEdit](https://stackedit.io/).
