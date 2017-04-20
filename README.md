![Xeekworx](http://xeekworx.com/images/github/xeekworx_logo.png) <br />
Autoversion
===========

**Autoversion is a command-line tool written in Python that looks for preprocessor definitions in a C/C++ header file and modifies the value to increment version values.**

Requirements:
1. Python 2.7 or 3.5 is needs to be installed on the system that uses this utility.
2. The only file you need from this repository is the command-line tool, "autoversion.py"

HOW IT WORKS
------------

As an example, if you give it the definition name *MYAPP_VERSION*, it will search (line by line) in the header file for that *#define* and increment any version values it detects. Multiple definition names can be given.

The format of the version should be, X.X.X.X, but each part is optional (so X.X is valid or even just X). The value separator can be a period or a comma. Version values can also be quoted. Below is an example of how autoversion interprets your version values:

    MAJOR.MINOR.REVISION.BUILD or 1.16.52.1

The version is incremented in this way ...

 1. **MAJOR**: Not incremented unless it is the only value in the version. If this is the only value in the version, it is incremented by + 1.
 2. **MINOR**: This is set to the two digit representation of the current year (eg. 16).
 3. **REVISION**: This is the month and day combined. If the current local date is May 2, the revision will be set to 52.
 4. **BUILD**: This is incremented by + 1.

The version separator (periods and commas), leading and trailing quotations, and trailing "\0" will be maintained when the version is modified.

Here's an example of C/C++ source code autoversion works with (or look at example.h):
``` cpp
#define MYAPP_PRODUCTVERSION 1,16,54,7
#define MYAPP_STRPRODUCTVERSION "1.16.54.7\0"
```

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
You can configure your Visual Studio project to run autoversion every time the project is built by following these instructions. Note that these instructions assumes your project is C/C++, other language projects will have different configurations.

 1. Right click on your project and select "Properties" or press ALT + ENTER with the project selected.
 2. Make sure the *Configuration* dropdown is set to "All Configurations" and that *Platform* is set to "All Platforms".
 3. On the left side select *Configuration Properties > Build Events > Pre-Build Event*.
 4. For the Command Line "autoversion.py "myversion.h MYDEF_PRODUCTVERSION"
 5. Make sure you put in the path for autoversion.py if it's not in the project's directory. Also make sure that you put in the path/filename of your header and the name of your #define in place of mine. Multiple definition arguments are possible.

![Visual Studio Screen Shot](http://xeekworx.com/images/github/autoversion/autoversion_screenshot.png)

> Written with [StackEdit](https://stackedit.io/).
