// The MIT License(MIT)
// Copyright(c) 2016 John Andrew Tullos(xeek@xeekworx.com)
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this
// software and associated documentation files(the "Software"), to deal in the Software
// without restriction, including without limitation the rights to use, copy, modify,
// merge, publish, distribute, sublicense, and / or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to the following
// conditions:
//
// The above copyright notice and this permission notice shall be included in all copies
// or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
// PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
// CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
// OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

// Example header file to use in testing autoversion.py
// The \0 is something that VS resource files used to require if these definitions
// were included within it for version info.

#define MYAPP_DEVSTAGE            "Alpha"
#define MYAPP_BUILDDATE			  1502823934
#define MYAPP_PRODUCTVERSION      1,17,815,0
#define MYAPP_STRPRODUCTVERSION   "1.17.815.0\0"
#define MYAPP_FILEVERSION         MYAPP_PRODUCTVERSION
#define MYAPP_STRFILEVERSION      MYAPP_STRPRODUCTVERSION
#define MYAPP_FILEDESC            "My Application"
#define MYAPP_PRODUCTNAME         "My Application\0"
#define MYAPP_AUTHOR              "John A. Tullos\0"
#define MYAPP_EMAIL               "xeek@xeekworx.com\0"
#define MYAPP_COMPANY             "Xeekworx\0"
#define MYAPP_COPYRIGHT           "Copyright © 2016 John Tullos. All Rights Reserved.\0"
#define MYAPP_COPYRIGHT_SHORT     "Copyright © 2016 John Tullos.\0"
#define MYAPP_CP_DETECT_TEST      "Copyright © 2015, 2016, 2016 John Tullos.\0"

