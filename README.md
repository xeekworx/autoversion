<img width="300" alt="Xeekworx" src="https://github.com/xeekworx/autoversion/raw/master/graphics/xeekworx_logo.png"><br />
<img width="300" alt="Autoversion" src="https://github.com/xeekworx/autoversion/raw/master/graphics/autoversion_logo.png">
===========

**Autoversion is a command-line tool written in Python that looks for preprocessor definitions in a C/C++ header file and modifies the value to increment version values.**

Requirements:
1. Python 2.7 or 3.5 is needs to be installed on the system that uses this utility.
2. The only file you need from this repository is the command-line tool, "autoversion.py"

HOW IT WORKS
------------

As an example, if you give it the definition name *MYAPP\_VERSION*, it will search (line by line) in the header file for that *#define* and increment any version values it detects. Multiple definition names can be given. If you notice any strangeness (\0) to my example header, it's because it's formatted to be used in version resources for Windows projects.

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

You can also keep the build date (timestamp) updated using the bdate\_macro option. The timestamp is a unixtime value that you can handle with time_t in C++. Here's an example of C/C++ source code autoversion works with for build dates (or look in exmaple.h):
``` cpp
#define MYAPP_BUILDDATE 1502827651
```

If you want to convert this build date value into something human readable, then it can be done with this sample code:
``` cpp
// Note: I'm using Microsoft versions of some calls to avoid compiler 
// warnings, whence the _s. This is C++, but it should be easy to convert 
// into standard C.

std::string get_builddate()
{
	// Get the build date in Unix Time:
	time_t unix_time = MYAPP_BUILDDATE;

	// Convert the Unix Time to Local Time:
	tm local_time = {};
	localtime_s(&local_time, &unix_time);

	// Convert the Local Time to a string:
	char tmp[48] = {};
	asctime_s(tmp, &local_time);
	
	// Remove newline (damn you asctime!):
	std::string result = tmp;
	result.pop_back();

	return result;
}
```

Another feature, the upcopyright option, lets you keep the year or years updated in all of your copyright macros. The algorithm searches for the case insensitive string "copyright" in either the macro name or the macro's value. If you add -l or --lastyear to your options then only the year found at the end of your macro value will be changed. This is handy for those copyrights that have ranges (eg. 2016 - 2017).
Here's what the macro might look like:
``` cpp
#define MYAPP_COPYRIGHT "Copyright © 2017 John Tullos. All Rights Reserved.\0"
```

COMMAND LINE
------------
```
usage: autoversion.py [--bdate_macro MACRO] [-c] [-l] [-p] [-v] [-?]
                      FILE [MACRO [MACRO ...]]

Autoversion is a Python command-line tool that looks for preprocessor
definitions in a C/C++ header file and modifies the value to increment version
values, etc.

positional arguments:
  FILE                 Source file to modify
  MACRO                Version macros to modify

optional arguments:
  --bdate_macro MACRO  Build date macro
  -c, --upcopyright    Update the year in copyrights
  -l, --lastyear       Update only the last year found in copyrights
  -p, --pyversion      Display Python version
  -v, --version        Display Autoversion version
  -?, --help
```

CONFIGURING VISUAL STUDIO (C/C++)
-----------------------------------
You can configure your Visual Studio project to run autoversion every time the project is built by following these instructions. Note that these instructions assumes your project is C/C++, other language projects will have different configurations.

 1. Right click on your project and select "Properties" or press ALT + ENTER with the project selected.
 2. Make sure the *Configuration* dropdown is set to "All Configurations" and that *Platform* is set to "All Platforms".
 3. On the left side select *Configuration Properties > Build Events > Pre-Build Event*.
 4. For the Command Line "autoversion.py "myversion.h MYDEF_PRODUCTVERSION"
 5. Make sure you put in the path for autoversion.py if it's not in the project's directory. Also make sure that you put in the path/filename of your header and the name of your #define in place of mine. Multiple definition arguments are possible.

![Visual Studio Screen Shot](http://xeekworx.com/images/github/autoversion/autoversion_screenshot.png)

