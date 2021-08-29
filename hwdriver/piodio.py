'''Wrapper for piodio.h

Generated with:
/usr/local/bin/ctypesgen.py -l/usr/ixpio/lib/libpio.so /usr/ixpio/include/piodio.h -o piodio.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["/usr/ixpio/lib/libpio.so"] = load_library("/usr/ixpio/lib/libpio.so")

# 1 libraries
# End libraries

# No modules

__pid_t = c_int # /usr/include/i386-linux-gnu/bits/types.h: 143

pid_t = __pid_t # /usr/include/i386-linux-gnu/sys/types.h: 99

__u8 = c_ubyte # /usr/include/asm-generic/int-ll64.h: 20

__u16 = c_ushort # /usr/include/asm-generic/int-ll64.h: 23

__u32 = c_uint # /usr/include/asm-generic/int-ll64.h: 26

__u64 = c_ulonglong # /usr/include/asm-generic/int-ll64.h: 33

ixpio_flags_t = c_uint # /usr/ixpio/include/_flags.h: 29

IXPIO_RESET_CONTROL_REGISTER = 0 # /usr/ixpio/include/ixpio.h: 238

IXPIO_AUX_CONTROL_REGISTER = (IXPIO_RESET_CONTROL_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_AUX_DATA_REGISTER = (IXPIO_AUX_CONTROL_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_INT_MASK_CONTROL_REGISTER = (IXPIO_AUX_DATA_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_AUX_PIN_STATUS_REGISTER = (IXPIO_INT_MASK_CONTROL_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_INTERRUPT_POLARITY_CONTROL_REGISTER = (IXPIO_AUX_PIN_STATUS_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8BIT_DATA_REGISTER = (IXPIO_INTERRUPT_POLARITY_CONTROL_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_ACTIVE_IO_PORT_CONTROL_REGISTER = (IXPIO_8BIT_DATA_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IO_SECECT_CONTROL_REGISTER = (IXPIO_ACTIVE_IO_PORT_CONTROL_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IO_SECECT_CONTROL_REGISTER_A = (IXPIO_IO_SECECT_CONTROL_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IO_SECECT_CONTROL_REGISTER_B = (IXPIO_IO_SECECT_CONTROL_REGISTER_A + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IO_SECECT_CONTROL_REGISTER_C = (IXPIO_IO_SECECT_CONTROL_REGISTER_B + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IO_SECECT_CONTROL_REGISTER_D = (IXPIO_IO_SECECT_CONTROL_REGISTER_C + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_PORT_A = (IXPIO_IO_SECECT_CONTROL_REGISTER_D + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_PORT_B = (IXPIO_8255_PORT_A + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_PORT_C = (IXPIO_8255_PORT_B + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_CONTROL_WORD = (IXPIO_8255_PORT_C + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_2_PORT_A = (IXPIO_8255_CONTROL_WORD + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_2_PORT_B = (IXPIO_8255_2_PORT_A + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_2_PORT_C = (IXPIO_8255_2_PORT_B + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8255_2_CONTROL_WORD = (IXPIO_8255_2_PORT_C + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_COUNTER_0 = (IXPIO_8255_2_CONTROL_WORD + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_COUNTER_1 = (IXPIO_8254_COUNTER_0 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_COUNTER_2 = (IXPIO_8254_COUNTER_1 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_CONTROL_WORD = (IXPIO_8254_COUNTER_2 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_2_COUNTER_0 = (IXPIO_8254_CONTROL_WORD + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_2_COUNTER_1 = (IXPIO_8254_2_COUNTER_0 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_2_COUNTER_2 = (IXPIO_8254_2_COUNTER_1 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_8254_2_CONTROL_WORD = (IXPIO_8254_2_COUNTER_2 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_CLOCK_INT_CONTROL_REGISTER = (IXPIO_8254_2_CONTROL_WORD + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IDIO0_TO_IDIO7 = (IXPIO_CLOCK_INT_CONTROL_REGISTER + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IDIO8_TO_IDIO15 = (IXPIO_IDIO0_TO_IDIO7 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_IDIO = (IXPIO_IDIO8_TO_IDIO15 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DIO0_TO_DIO7 = (IXPIO_IDIO + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DIO8_TO_DIO15 = (IXPIO_DIO0_TO_DIO7 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DIO16_TO_DIO23 = (IXPIO_DIO8_TO_DIO15 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DIO24_TO_DIO31 = (IXPIO_DIO16_TO_DIO23 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DIO = (IXPIO_DIO24_TO_DIO31 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI0_TO_DI7 = (IXPIO_DIO + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI8_TO_DI15 = (IXPIO_DI0_TO_DI7 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI16_TO_DI23 = (IXPIO_DI8_TO_DI15 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI24_TO_DI31 = (IXPIO_DI16_TO_DI23 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI32_TO_DI39 = (IXPIO_DI24_TO_DI31 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI40_TO_DI47 = (IXPIO_DI32_TO_DI39 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI48_TO_DI55 = (IXPIO_DI40_TO_DI47 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI56_TO_DI63 = (IXPIO_DI48_TO_DI55 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DI = (IXPIO_DI56_TO_DI63 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO0_TO_DO7 = (IXPIO_DI + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO8_TO_DO15 = (IXPIO_DO0_TO_DO7 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO16_TO_DO23 = (IXPIO_DO8_TO_DO15 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO24_TO_DO31 = (IXPIO_DO16_TO_DO23 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO32_TO_DO39 = (IXPIO_DO24_TO_DO31 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO40_TO_DO47 = (IXPIO_DO32_TO_DO39 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO48_TO_DO55 = (IXPIO_DO40_TO_DO47 + 1) # /usr/ixpio/include/ixpio.h: 238

IXPIO_DO56_TO_DO63 = (IXPIO_DO48_TO_DO55 + 1) # /usr/ixpio/include/ixpio.h: 238

# /usr/ixpio/include/ixpio.h: 549
class union_data(Union):
    pass

union_data.__slots__ = [
    'u8',
    'u16',
    'u32',
    'u64',
    'ptr',
]
union_data._fields_ = [
    ('u8', __u8),
    ('u16', __u16),
    ('u32', __u32),
    ('u64', __u64),
    ('ptr', POINTER(None)),
]

data_t = union_data # /usr/ixpio/include/ixpio.h: 549

# /usr/ixpio/include/ixpio.h: 552
class struct_ixpio_signal(Structure):
    pass

# /usr/ixpio/include/ixpio.h: 558
class struct_task_struct(Structure):
    pass

struct_ixpio_signal.__slots__ = [
    'prev',
    'next',
    'id',
    'sid',
    'pid',
    'task',
    '_is',
    'edge',
    'bedge',
]
struct_ixpio_signal._fields_ = [
    ('prev', POINTER(struct_ixpio_signal)),
    ('next', POINTER(struct_ixpio_signal)),
    ('id', c_int),
    ('sid', c_int),
    ('pid', pid_t),
    ('task', POINTER(struct_task_struct)),
    ('_is', c_int),
    ('edge', c_int),
    ('bedge', c_int),
]

ixpio_signal_t = struct_ixpio_signal # /usr/ixpio/include/ixpio.h: 569

# /usr/ixpio/include/ixpio.h: 575
class struct_ixpio_reg(Structure):
    pass

struct_ixpio_reg.__slots__ = [
    'id',
    'value',
]
struct_ixpio_reg._fields_ = [
    ('id', c_uint),
    ('value', c_uint),
]

ixpio_reg_t = struct_ixpio_reg # /usr/ixpio/include/ixpio.h: 575

# /usr/ixpio/include/ixpio.h: 581
class struct_ixpio_analog(Structure):
    pass

struct_ixpio_analog.__slots__ = [
    'prev',
    'next',
    'id',
    'sig',
    'channel',
    'flags',
    'data_size',
    'data_cur',
    'data',
]
struct_ixpio_analog._fields_ = [
    ('prev', POINTER(struct_ixpio_analog)),
    ('next', POINTER(struct_ixpio_analog)),
    ('id', c_uint),
    ('sig', ixpio_signal_t),
    ('channel', c_uint),
    ('flags', ixpio_flags_t),
    ('data_size', c_uint),
    ('data_cur', c_uint),
    ('data', data_t),
]

ixpio_analog_t = struct_ixpio_analog # /usr/ixpio/include/ixpio.h: 591

WORD = c_ushort # /usr/ixpio/include/piodio.h: 145

HANDLE = CFUNCTYPE(UNCHECKED(None), c_int) # /usr/ixpio/include/piodio.h: 146

byte = c_ubyte # /usr/ixpio/include/piodio.h: 147

boolean = c_int # /usr/ixpio/include/piodio.h: 148

# /usr/ixpio/include/piodio.h: 150
class struct_port_list(Structure):
    pass

struct_port_list.__slots__ = [
    'ports',
]
struct_port_list._fields_ = [
    ('ports', WORD * 6),
]

# /usr/ixpio/include/piodio.h: 159
class struct_port_config(Structure):
    pass

struct_port_config.__slots__ = [
    'init',
    'id',
    'status',
]
struct_port_config._fields_ = [
    ('init', WORD),
    ('id', WORD),
    ('status', WORD),
]

port_config_t = struct_port_config # /usr/ixpio/include/piodio.h: 159

# /usr/ixpio/include/piodio.h: 176
class struct_dev_control(Structure):
    pass

struct_dev_control.__slots__ = [
    'pconf',
    'deviceinit',
    'portdircfs',
    'doutput',
    'doutput_port',
    'dinput',
    'dinput_port',
    'int_source_init',
    'ainput',
]
struct_dev_control._fields_ = [
    ('pconf', port_config_t * 4),
    ('deviceinit', CFUNCTYPE(UNCHECKED(WORD), WORD, WORD)),
    ('portdircfs', CFUNCTYPE(UNCHECKED(WORD), WORD, WORD, boolean)),
    ('doutput', CFUNCTYPE(UNCHECKED(WORD), WORD, byte)),
    ('doutput_port', CFUNCTYPE(UNCHECKED(WORD), WORD, WORD, byte)),
    ('dinput', CFUNCTYPE(UNCHECKED(WORD), WORD, POINTER(WORD))),
    ('dinput_port', CFUNCTYPE(UNCHECKED(WORD), WORD, WORD, POINTER(WORD))),
    ('int_source_init', CFUNCTYPE(UNCHECKED(WORD), WORD, WORD, WORD)),
    ('ainput', CFUNCTYPE(UNCHECKED(WORD), WORD, WORD, WORD, POINTER(c_float))),
]

dev_control_t = struct_dev_control # /usr/ixpio/include/piodio.h: 176

# /usr/ixpio/include/piodio.h: 180
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_Open'):
    PIODA_Open = _libs['/usr/ixpio/lib/libpio.so'].PIODA_Open
    PIODA_Open.argtypes = [String]
    PIODA_Open.restype = c_int

# /usr/ixpio/include/piodio.h: 181
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_Close'):
    PIODA_Close = _libs['/usr/ixpio/lib/libpio.so'].PIODA_Close
    PIODA_Close.argtypes = [WORD]
    PIODA_Close.restype = WORD

# /usr/ixpio/include/piodio.h: 182
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_DriverInit'):
    PIODA_DriverInit = _libs['/usr/ixpio/lib/libpio.so'].PIODA_DriverInit
    PIODA_DriverInit.argtypes = [WORD]
    PIODA_DriverInit.restype = WORD

# /usr/ixpio/include/piodio.h: 183
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_GetDriverVersion'):
    PIODA_GetDriverVersion = _libs['/usr/ixpio/lib/libpio.so'].PIODA_GetDriverVersion
    PIODA_GetDriverVersion.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        PIODA_GetDriverVersion.restype = ReturnString
    else:
        PIODA_GetDriverVersion.restype = String
        PIODA_GetDriverVersion.errcheck = ReturnString

# /usr/ixpio/include/piodio.h: 184
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_GetLibraryVersion'):
    PIODA_GetLibraryVersion = _libs['/usr/ixpio/lib/libpio.so'].PIODA_GetLibraryVersion
    PIODA_GetLibraryVersion.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        PIODA_GetLibraryVersion.restype = ReturnString
    else:
        PIODA_GetLibraryVersion.restype = String
        PIODA_GetLibraryVersion.errcheck = ReturnString

# /usr/ixpio/include/piodio.h: 185
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_DeviceInit'):
    PIODA_DeviceInit = _libs['/usr/ixpio/lib/libpio.so'].PIODA_DeviceInit
    PIODA_DeviceInit.argtypes = [WORD]
    PIODA_DeviceInit.restype = WORD

# /usr/ixpio/include/piodio.h: 186
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_PortDirCfs'):
    PIODA_PortDirCfs = _libs['/usr/ixpio/lib/libpio.so'].PIODA_PortDirCfs
    PIODA_PortDirCfs.argtypes = [WORD, WORD, boolean]
    PIODA_PortDirCfs.restype = WORD

# /usr/ixpio/include/piodio.h: 187
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_Digital_Output'):
    PIODA_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PIODA_Digital_Output
    PIODA_Digital_Output.argtypes = [WORD, WORD, byte]
    PIODA_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 188
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_Digital_Input'):
    PIODA_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PIODA_Digital_Input
    PIODA_Digital_Input.argtypes = [WORD, WORD, POINTER(WORD)]
    PIODA_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 189
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_IntInstall'):
    PIODA_IntInstall = _libs['/usr/ixpio/lib/libpio.so'].PIODA_IntInstall
    PIODA_IntInstall.argtypes = [WORD, HANDLE, WORD, WORD, WORD]
    PIODA_IntInstall.restype = WORD

# /usr/ixpio/include/piodio.h: 190
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_IntRemove'):
    PIODA_IntRemove = _libs['/usr/ixpio/lib/libpio.so'].PIODA_IntRemove
    PIODA_IntRemove.argtypes = [WORD, WORD]
    PIODA_IntRemove.restype = WORD

# /usr/ixpio/include/piodio.h: 191
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_OutputByte'):
    PIODA_OutputByte = _libs['/usr/ixpio/lib/libpio.so'].PIODA_OutputByte
    PIODA_OutputByte.argtypes = [WORD, POINTER(ixpio_reg_t)]
    PIODA_OutputByte.restype = WORD

# /usr/ixpio/include/piodio.h: 192
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_InputByte'):
    PIODA_InputByte = _libs['/usr/ixpio/lib/libpio.so'].PIODA_InputByte
    PIODA_InputByte.argtypes = [WORD, POINTER(ixpio_reg_t)]
    PIODA_InputByte.restype = WORD

# /usr/ixpio/include/piodio.h: 193
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_OutputAnalog'):
    PIODA_OutputAnalog = _libs['/usr/ixpio/lib/libpio.so'].PIODA_OutputAnalog
    PIODA_OutputAnalog.argtypes = [WORD, POINTER(ixpio_analog_t)]
    PIODA_OutputAnalog.restype = WORD

# /usr/ixpio/include/piodio.h: 196
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'PIODA_SetChannelConfig'):
        continue
    PIODA_SetChannelConfig = _lib.PIODA_SetChannelConfig
    PIODA_SetChannelConfig.argtypes = [WORD, WORD, WORD]
    PIODA_SetChannelConfig.restype = WORD
    break

# /usr/ixpio/include/piodio.h: 197
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'PIODA_AnalogOutputHex'):
        continue
    PIODA_AnalogOutputHex = _lib.PIODA_AnalogOutputHex
    PIODA_AnalogOutputHex.argtypes = [WORD, WORD, WORD]
    PIODA_AnalogOutputHex.restype = WORD
    break

# /usr/ixpio/include/piodio.h: 198
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'PIODA_AnalogInputHex'):
        continue
    PIODA_AnalogInputHex = _lib.PIODA_AnalogInputHex
    PIODA_AnalogInputHex.argtypes = [WORD, WORD, POINTER(WORD)]
    PIODA_AnalogInputHex.restype = WORD
    break

# /usr/ixpio/include/piodio.h: 199
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_AnalogOutputVoltage'):
    PIODA_AnalogOutputVoltage = _libs['/usr/ixpio/lib/libpio.so'].PIODA_AnalogOutputVoltage
    PIODA_AnalogOutputVoltage.argtypes = [WORD, WORD, c_float]
    PIODA_AnalogOutputVoltage.restype = WORD

# /usr/ixpio/include/piodio.h: 200
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_AnalogOutputCalVoltage'):
    PIODA_AnalogOutputCalVoltage = _libs['/usr/ixpio/lib/libpio.so'].PIODA_AnalogOutputCalVoltage
    PIODA_AnalogOutputCalVoltage.argtypes = [WORD, WORD, c_float]
    PIODA_AnalogOutputCalVoltage.restype = WORD

# /usr/ixpio/include/piodio.h: 201
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_AnalogOutputCurrent'):
    PIODA_AnalogOutputCurrent = _libs['/usr/ixpio/lib/libpio.so'].PIODA_AnalogOutputCurrent
    PIODA_AnalogOutputCurrent.argtypes = [WORD, WORD, c_float]
    PIODA_AnalogOutputCurrent.restype = WORD

# /usr/ixpio/include/piodio.h: 202
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_AnalogOutputCalCurrent'):
    PIODA_AnalogOutputCalCurrent = _libs['/usr/ixpio/lib/libpio.so'].PIODA_AnalogOutputCalCurrent
    PIODA_AnalogOutputCalCurrent.argtypes = [WORD, WORD, c_float]
    PIODA_AnalogOutputCalCurrent.restype = WORD

# /usr/ixpio/include/piodio.h: 203
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA_AnalogInputVoltage'):
    PIODA_AnalogInputVoltage = _libs['/usr/ixpio/lib/libpio.so'].PIODA_AnalogInputVoltage
    PIODA_AnalogInputVoltage.argtypes = [WORD, WORD, WORD, POINTER(c_float)]
    PIODA_AnalogInputVoltage.restype = WORD

# /usr/ixpio/include/piodio.h: 208
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD144_168_DeviceInit'):
    PIOD144_168_DeviceInit = _libs['/usr/ixpio/lib/libpio.so'].PIOD144_168_DeviceInit
    PIOD144_168_DeviceInit.argtypes = [WORD, WORD]
    PIOD144_168_DeviceInit.restype = WORD

# /usr/ixpio/include/piodio.h: 209
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD144_168_PortDirCfs'):
    PIOD144_168_PortDirCfs = _libs['/usr/ixpio/lib/libpio.so'].PIOD144_168_PortDirCfs
    PIOD144_168_PortDirCfs.argtypes = [WORD, WORD, boolean]
    PIOD144_168_PortDirCfs.restype = WORD

# /usr/ixpio/include/piodio.h: 210
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD144_168_Digital_Output'):
    PIOD144_168_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PIOD144_168_Digital_Output
    PIOD144_168_Digital_Output.argtypes = [WORD, WORD, byte]
    PIOD144_168_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 211
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD144_168_Digital_Input'):
    PIOD144_168_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PIOD144_168_Digital_Input
    PIOD144_168_Digital_Input.argtypes = [WORD, WORD, POINTER(WORD)]
    PIOD144_168_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 212
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD144_168_Int_Source_Init'):
    PIOD144_168_Int_Source_Init = _libs['/usr/ixpio/lib/libpio.so'].PIOD144_168_Int_Source_Init
    PIOD144_168_Int_Source_Init.argtypes = [WORD, WORD, WORD]
    PIOD144_168_Int_Source_Init.restype = WORD

# /usr/ixpio/include/piodio.h: 215
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD56_24_PortDirCfs'):
    PIOD56_24_PortDirCfs = _libs['/usr/ixpio/lib/libpio.so'].PIOD56_24_PortDirCfs
    PIOD56_24_PortDirCfs.argtypes = [WORD, WORD, boolean]
    PIOD56_24_PortDirCfs.restype = WORD

# /usr/ixpio/include/piodio.h: 216
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD56_24_Digital_Output'):
    PIOD56_24_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PIOD56_24_Digital_Output
    PIOD56_24_Digital_Output.argtypes = [WORD, WORD, byte]
    PIOD56_24_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 217
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD56_24_Digital_Input'):
    PIOD56_24_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PIOD56_24_Digital_Input
    PIOD56_24_Digital_Input.argtypes = [WORD, WORD, POINTER(WORD)]
    PIOD56_24_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 218
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD56_24_Int_Source_Init'):
    PIOD56_24_Int_Source_Init = _libs['/usr/ixpio/lib/libpio.so'].PIOD56_24_Int_Source_Init
    PIOD56_24_Int_Source_Init.argtypes = [WORD, WORD, WORD]
    PIOD56_24_Int_Source_Init.restype = WORD

# /usr/ixpio/include/piodio.h: 221
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD96_PortDirCfs'):
    PIOD96_PortDirCfs = _libs['/usr/ixpio/lib/libpio.so'].PIOD96_PortDirCfs
    PIOD96_PortDirCfs.argtypes = [WORD, WORD, boolean]
    PIOD96_PortDirCfs.restype = WORD

# /usr/ixpio/include/piodio.h: 222
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD96_Digital_Output'):
    PIOD96_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PIOD96_Digital_Output
    PIOD96_Digital_Output.argtypes = [WORD, WORD, byte]
    PIOD96_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 223
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD96_Digital_Input'):
    PIOD96_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PIOD96_Digital_Input
    PIOD96_Digital_Input.argtypes = [WORD, WORD, POINTER(WORD)]
    PIOD96_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 224
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIOD96_Int_Source_Init'):
    PIOD96_Int_Source_Init = _libs['/usr/ixpio/lib/libpio.so'].PIOD96_Int_Source_Init
    PIOD96_Int_Source_Init.argtypes = [WORD, WORD, WORD]
    PIOD96_Int_Source_Init.restype = WORD

# /usr/ixpio/include/piodio.h: 227
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISOP8R8_Digital_Output'):
    PISOP8R8_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PISOP8R8_Digital_Output
    PISOP8R8_Digital_Output.argtypes = [WORD, byte]
    PISOP8R8_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 228
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISOP8R8_Digital_Input'):
    PISOP8R8_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PISOP8R8_Digital_Input
    PISOP8R8_Digital_Input.argtypes = [WORD, POINTER(WORD)]
    PISOP8R8_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 231
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISO725_Digital_Output'):
    PISO725_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PISO725_Digital_Output
    PISO725_Digital_Output.argtypes = [WORD, byte]
    PISO725_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 232
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISO725_Digital_Input'):
    PISO725_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PISO725_Digital_Input
    PISO725_Digital_Input.argtypes = [WORD, POINTER(WORD)]
    PISO725_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 233
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISO725_Int_Source_Init'):
    PISO725_Int_Source_Init = _libs['/usr/ixpio/lib/libpio.so'].PISO725_Int_Source_Init
    PISO725_Int_Source_Init.argtypes = [WORD, WORD, WORD]
    PISO725_Int_Source_Init.restype = WORD

# /usr/ixpio/include/piodio.h: 236
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISOA64_C64_Digital_Output'):
    PISOA64_C64_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PISOA64_C64_Digital_Output
    PISOA64_C64_Digital_Output.argtypes = [WORD, WORD, byte]
    PISOA64_C64_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 237
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISOP64_Digital_Input'):
    PISOP64_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PISOP64_Digital_Input
    PISOP64_Digital_Input.argtypes = [WORD, WORD, POINTER(WORD)]
    PISOP64_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 238
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISOP32A32_C32_Digital_Output'):
    PISOP32A32_C32_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PISOP32A32_C32_Digital_Output
    PISOP32A32_C32_Digital_Output.argtypes = [WORD, WORD, byte]
    PISOP32A32_C32_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 239
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISOP32A32_C32_Digital_Input'):
    PISOP32A32_C32_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PISOP32A32_C32_Digital_Input
    PISOP32A32_C32_Digital_Input.argtypes = [WORD, WORD, POINTER(WORD)]
    PISOP32A32_C32_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 242
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA16_Digital_Output'):
    PIODA16_Digital_Output = _libs['/usr/ixpio/lib/libpio.so'].PIODA16_Digital_Output
    PIODA16_Digital_Output.argtypes = [WORD, byte]
    PIODA16_Digital_Output.restype = WORD

# /usr/ixpio/include/piodio.h: 243
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA16_Digital_Input'):
    PIODA16_Digital_Input = _libs['/usr/ixpio/lib/libpio.so'].PIODA16_Digital_Input
    PIODA16_Digital_Input.argtypes = [WORD, POINTER(WORD)]
    PIODA16_Digital_Input.restype = WORD

# /usr/ixpio/include/piodio.h: 244
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PIODA16_Int_Source_Init'):
    PIODA16_Int_Source_Init = _libs['/usr/ixpio/lib/libpio.so'].PIODA16_Int_Source_Init
    PIODA16_Int_Source_Init.argtypes = [WORD, WORD, WORD]
    PIODA16_Int_Source_Init.restype = WORD

# /usr/ixpio/include/piodio.h: 247
if hasattr(_libs['/usr/ixpio/lib/libpio.so'], 'PISO813_Analog_Input_Voltage'):
    PISO813_Analog_Input_Voltage = _libs['/usr/ixpio/lib/libpio.so'].PISO813_Analog_Input_Voltage
    PISO813_Analog_Input_Voltage.argtypes = [WORD, WORD, WORD, POINTER(c_float)]
    PISO813_Analog_Input_Voltage.restype = WORD

# /usr/ixpio/include/ixpio.h: 442
try:
    IXPIO_DIO_A = IXPIO_DIO0_TO_DIO7
except:
    pass

# /usr/ixpio/include/ixpio.h: 443
try:
    IXPIO_DIO_B = IXPIO_DIO8_TO_DIO15
except:
    pass

# /usr/ixpio/include/ixpio.h: 444
try:
    IXPIO_DIO_C = IXPIO_DIO16_TO_DIO23
except:
    pass

# /usr/ixpio/include/ixpio.h: 445
try:
    IXPIO_DIO_D = IXPIO_DIO24_TO_DIO31
except:
    pass

# /usr/ixpio/include/ixpio.h: 447
try:
    IXPIO_DI_A = IXPIO_DI0_TO_DI7
except:
    pass

# /usr/ixpio/include/ixpio.h: 448
try:
    IXPIO_DI_B = IXPIO_DI8_TO_DI15
except:
    pass

# /usr/ixpio/include/ixpio.h: 449
try:
    IXPIO_DI_C = IXPIO_DI16_TO_DI23
except:
    pass

# /usr/ixpio/include/ixpio.h: 450
try:
    IXPIO_DI_D = IXPIO_DI24_TO_DI31
except:
    pass

# /usr/ixpio/include/ixpio.h: 451
try:
    IXPIO_DI_E = IXPIO_DI32_TO_DI39
except:
    pass

# /usr/ixpio/include/ixpio.h: 452
try:
    IXPIO_DI_F = IXPIO_DI40_TO_DI47
except:
    pass

# /usr/ixpio/include/ixpio.h: 453
try:
    IXPIO_DI_G = IXPIO_DI48_TO_DI55
except:
    pass

# /usr/ixpio/include/ixpio.h: 454
try:
    IXPIO_DI_H = IXPIO_DI56_TO_DI63
except:
    pass

# /usr/ixpio/include/ixpio.h: 456
try:
    IXPIO_DO_A = IXPIO_DO0_TO_DO7
except:
    pass

# /usr/ixpio/include/ixpio.h: 457
try:
    IXPIO_DO_B = IXPIO_DO8_TO_DO15
except:
    pass

# /usr/ixpio/include/ixpio.h: 458
try:
    IXPIO_DO_C = IXPIO_DO16_TO_DO23
except:
    pass

# /usr/ixpio/include/ixpio.h: 459
try:
    IXPIO_DO_D = IXPIO_DO24_TO_DO31
except:
    pass

# /usr/ixpio/include/ixpio.h: 460
try:
    IXPIO_DO_E = IXPIO_DO32_TO_DO39
except:
    pass

# /usr/ixpio/include/ixpio.h: 461
try:
    IXPIO_DO_F = IXPIO_DO40_TO_DO47
except:
    pass

# /usr/ixpio/include/ixpio.h: 462
try:
    IXPIO_DO_G = IXPIO_DO48_TO_DO55
except:
    pass

# /usr/ixpio/include/ixpio.h: 463
try:
    IXPIO_DO_H = IXPIO_DO56_TO_DO63
except:
    pass

# /usr/ixpio/include/piodio.h: 13
try:
    PIODA_NOERROR = 0
except:
    pass

# /usr/ixpio/include/piodio.h: 14
try:
    PIODA_MODULE_NAME_GET_ERROR = 1
except:
    pass

# /usr/ixpio/include/piodio.h: 15
try:
    PIODA_DEVICE_DIO_INIT_ERROR = 2
except:
    pass

# /usr/ixpio/include/piodio.h: 16
try:
    PIODA_ACTIVE_PORT_ERROR = 3
except:
    pass

# /usr/ixpio/include/piodio.h: 17
try:
    PIODA_PORT_DEFINED_ERROR = 4
except:
    pass

# /usr/ixpio/include/piodio.h: 18
try:
    PIODA_DIGITAL_OUTPUT_ERROR = 5
except:
    pass

# /usr/ixpio/include/piodio.h: 19
try:
    PIODA_DIGITAL_INPUT_ERROR = 6
except:
    pass

# /usr/ixpio/include/piodio.h: 20
try:
    PIODA_INT_SOURCE_DEFINED_ERROR = 7
except:
    pass

# /usr/ixpio/include/piodio.h: 21
try:
    PIODA_CONFIGURE_INTERRUPT_ERROR = 8
except:
    pass

# /usr/ixpio/include/piodio.h: 22
try:
    PIODA_ACTIVEMODE_DEFINED_ERROR = 9
except:
    pass

# /usr/ixpio/include/piodio.h: 23
try:
    PIODA_ADD_SIGNAL_ERROR = 10
except:
    pass

# /usr/ixpio/include/piodio.h: 24
try:
    PIODA_AUX_CONTROL_ERROR = 11
except:
    pass

# /usr/ixpio/include/piodio.h: 25
try:
    PIODA_AUX_DATA_ERROR = 12
except:
    pass

# /usr/ixpio/include/piodio.h: 26
try:
    PIODA_READ_EEPROM_ERROR = 13
except:
    pass

# /usr/ixpio/include/piodio.h: 27
try:
    PIODA_EEPROM_DATA_ERROR = 14
except:
    pass

# /usr/ixpio/include/piodio.h: 28
try:
    PIODA_OUTPUT_VOLTAGE_ERROR = 115
except:
    pass

# /usr/ixpio/include/piodio.h: 29
try:
    PIODA_OUTPUT_CALVOLTAGE_ERROR = 116
except:
    pass

# /usr/ixpio/include/piodio.h: 30
try:
    PIODA_OUTPUT_CURRENT_ERROR = 17
except:
    pass

# /usr/ixpio/include/piodio.h: 31
try:
    PIODA_OUTPUT_CALCURRENT_ERROR = 18
except:
    pass

# /usr/ixpio/include/piodio.h: 32
try:
    PIODA_ANALOG_INPUT_VOLTAGE_ERROR = 19
except:
    pass

# /usr/ixpio/include/piodio.h: 33
try:
    PIODA_SET_GAIN_ERROR = 20
except:
    pass

# /usr/ixpio/include/piodio.h: 34
try:
    PIODA_SET_CHANNEL_ERROR = 21
except:
    pass

# /usr/ixpio/include/piodio.h: 35
try:
    PIODA_LIBRARY_ARGUMENT_ERROR = 22
except:
    pass

# /usr/ixpio/include/piodio.h: 38
try:
    IXPIO_DRIVER_VERSION = '0.22.1'
except:
    pass

# /usr/ixpio/include/piodio.h: 39
try:
    IXPIO_LIBRARY_VERSION = '0.3.0'
except:
    pass

# /usr/ixpio/include/piodio.h: 41
try:
    LINE_SIZE = 128
except:
    pass

# /usr/ixpio/include/piodio.h: 42
try:
    MAX_BOARD_NUMBER = 30
except:
    pass

# /usr/ixpio/include/piodio.h: 43
try:
    MAX_CARD_SUPPORT = 4
except:
    pass

# /usr/ixpio/include/piodio.h: 44
try:
    MAX_PORT_LEVEL = 4
except:
    pass

# /usr/ixpio/include/piodio.h: 45
try:
    LEVEL_A = 0
except:
    pass

# /usr/ixpio/include/piodio.h: 46
try:
    LEVEL_B = 1
except:
    pass

# /usr/ixpio/include/piodio.h: 47
try:
    LEVEL_C = 2
except:
    pass

# /usr/ixpio/include/piodio.h: 48
try:
    LEVEL_D = 3
except:
    pass

# /usr/ixpio/include/piodio.h: 51
try:
    DIGITAL_OUTPUT = 0
except:
    pass

# /usr/ixpio/include/piodio.h: 52
try:
    DIGITAL_INPUT = 1
except:
    pass

# /usr/ixpio/include/piodio.h: 55
try:
    P2C0 = 1
except:
    pass

# /usr/ixpio/include/piodio.h: 56
try:
    P2C1 = 2
except:
    pass

# /usr/ixpio/include/piodio.h: 57
try:
    P2C2 = 4
except:
    pass

# /usr/ixpio/include/piodio.h: 58
try:
    P2C3 = 8
except:
    pass

# /usr/ixpio/include/piodio.h: 59
try:
    ALL_INT = 15
except:
    pass

# /usr/ixpio/include/piodio.h: 62
try:
    PIOD144_168_P2C0 = P2C0
except:
    pass

# /usr/ixpio/include/piodio.h: 63
try:
    PIOD144_168_P2C1 = P2C1
except:
    pass

# /usr/ixpio/include/piodio.h: 64
try:
    PIOD144_168_P2C2 = P2C2
except:
    pass

# /usr/ixpio/include/piodio.h: 65
try:
    PIOD144_168_P2C3 = P2C3
except:
    pass

# /usr/ixpio/include/piodio.h: 66
try:
    PIOD144_168_ALL_INT = ALL_INT
except:
    pass

# /usr/ixpio/include/piodio.h: 69
try:
    PIODA16_INT0 = 1
except:
    pass

# /usr/ixpio/include/piodio.h: 70
try:
    PIODA16_INT1 = 2
except:
    pass

# /usr/ixpio/include/piodio.h: 71
try:
    PIODA16_ALL_INT = 3
except:
    pass

# /usr/ixpio/include/piodio.h: 74
try:
    PISO725_INT0 = 1
except:
    pass

# /usr/ixpio/include/piodio.h: 75
try:
    PISO725_INT1 = 2
except:
    pass

# /usr/ixpio/include/piodio.h: 76
try:
    PISO725_INT2 = 4
except:
    pass

# /usr/ixpio/include/piodio.h: 77
try:
    PISO725_INT3 = 8
except:
    pass

# /usr/ixpio/include/piodio.h: 78
try:
    PISO725_INT4 = 16
except:
    pass

# /usr/ixpio/include/piodio.h: 79
try:
    PISO725_INT5 = 32
except:
    pass

# /usr/ixpio/include/piodio.h: 80
try:
    PISO725_INT6 = 64
except:
    pass

# /usr/ixpio/include/piodio.h: 81
try:
    PISO725_INT7 = 128
except:
    pass

# /usr/ixpio/include/piodio.h: 82
try:
    PISO725_ALL_INT = 255
except:
    pass

# /usr/ixpio/include/piodio.h: 85
try:
    PIOD96_P2C0 = P2C0
except:
    pass

# /usr/ixpio/include/piodio.h: 86
try:
    PIOD96_P2C1 = P2C1
except:
    pass

# /usr/ixpio/include/piodio.h: 87
try:
    PIOD96_P5C0 = PIOD96_P2C1
except:
    pass

# /usr/ixpio/include/piodio.h: 88
try:
    PIOD96_P2C2 = P2C2
except:
    pass

# /usr/ixpio/include/piodio.h: 89
try:
    PIOD96_P8C0 = PIOD96_P2C2
except:
    pass

# /usr/ixpio/include/piodio.h: 90
try:
    PIOD96_P2C3 = P2C3
except:
    pass

# /usr/ixpio/include/piodio.h: 91
try:
    PIOD96_P11C0 = PIOD96_P2C3
except:
    pass

# /usr/ixpio/include/piodio.h: 92
try:
    PIOD96_ALL_INT = ALL_INT
except:
    pass

# /usr/ixpio/include/piodio.h: 95
try:
    PIOD56_24_P2C0 = P2C0
except:
    pass

# /usr/ixpio/include/piodio.h: 96
try:
    PIOD56_24_P2C1 = P2C1
except:
    pass

# /usr/ixpio/include/piodio.h: 97
try:
    PIOD56_24_P2C2 = P2C2
except:
    pass

# /usr/ixpio/include/piodio.h: 98
try:
    PIOD56_24_P2C3 = P2C3
except:
    pass

# /usr/ixpio/include/piodio.h: 99
try:
    PIOD56_24_ALL_INT = ALL_INT
except:
    pass

# /usr/ixpio/include/piodio.h: 102
try:
    PISOP64_DIA = IXPIO_DI_A
except:
    pass

# /usr/ixpio/include/piodio.h: 103
try:
    PISOP64_DIB = IXPIO_DI_B
except:
    pass

# /usr/ixpio/include/piodio.h: 104
try:
    PISOP64_DIC = IXPIO_DI_C
except:
    pass

# /usr/ixpio/include/piodio.h: 105
try:
    PISOP64_DID = IXPIO_DI_D
except:
    pass

# /usr/ixpio/include/piodio.h: 106
try:
    PISOP64_DIE = IXPIO_DI_E
except:
    pass

# /usr/ixpio/include/piodio.h: 107
try:
    PISOP64_DIF = IXPIO_DI_F
except:
    pass

# /usr/ixpio/include/piodio.h: 108
try:
    PISOP64_DIG = IXPIO_DI_G
except:
    pass

# /usr/ixpio/include/piodio.h: 109
try:
    PISOP64_DIH = IXPIO_DI_H
except:
    pass

# /usr/ixpio/include/piodio.h: 112
try:
    PISOA64_DOA = IXPIO_DO_A
except:
    pass

# /usr/ixpio/include/piodio.h: 113
try:
    PISOA64_DOB = IXPIO_DO_B
except:
    pass

# /usr/ixpio/include/piodio.h: 114
try:
    PISOA64_DOC = IXPIO_DO_C
except:
    pass

# /usr/ixpio/include/piodio.h: 115
try:
    PISOA64_DOD = IXPIO_DO_D
except:
    pass

# /usr/ixpio/include/piodio.h: 116
try:
    PISOA64_DOE = IXPIO_DO_E
except:
    pass

# /usr/ixpio/include/piodio.h: 117
try:
    PISOA64_DOF = IXPIO_DO_F
except:
    pass

# /usr/ixpio/include/piodio.h: 118
try:
    PISOA64_DOG = IXPIO_DO_G
except:
    pass

# /usr/ixpio/include/piodio.h: 119
try:
    PISOA64_DOH = IXPIO_DO_H
except:
    pass

# /usr/ixpio/include/piodio.h: 122
try:
    PISOC64_DOA = IXPIO_DO_A
except:
    pass

# /usr/ixpio/include/piodio.h: 123
try:
    PISOC64_DOB = IXPIO_DO_B
except:
    pass

# /usr/ixpio/include/piodio.h: 124
try:
    PISOC64_DOC = IXPIO_DO_C
except:
    pass

# /usr/ixpio/include/piodio.h: 125
try:
    PISOC64_DOD = IXPIO_DO_D
except:
    pass

# /usr/ixpio/include/piodio.h: 126
try:
    PISOC64_DOE = IXPIO_DO_E
except:
    pass

# /usr/ixpio/include/piodio.h: 127
try:
    PISOC64_DOF = IXPIO_DO_F
except:
    pass

# /usr/ixpio/include/piodio.h: 128
try:
    PISOC64_DOG = IXPIO_DO_G
except:
    pass

# /usr/ixpio/include/piodio.h: 129
try:
    PISOC64_DOH = IXPIO_DO_H
except:
    pass

# /usr/ixpio/include/piodio.h: 132
try:
    PISOP32C32_DIOA = IXPIO_DIO_A
except:
    pass

# /usr/ixpio/include/piodio.h: 133
try:
    PISOP32C32_DIOB = IXPIO_DIO_B
except:
    pass

# /usr/ixpio/include/piodio.h: 134
try:
    PISOP32C32_DIOC = IXPIO_DIO_C
except:
    pass

# /usr/ixpio/include/piodio.h: 135
try:
    PISOP32C32_DIOD = IXPIO_DIO_D
except:
    pass

# /usr/ixpio/include/piodio.h: 136
try:
    PISOP32C32_DIO_ALL = IXPIO_DIO
except:
    pass

# /usr/ixpio/include/piodio.h: 139
try:
    PISOP32A32_DIOA = IXPIO_DIO_A
except:
    pass

# /usr/ixpio/include/piodio.h: 140
try:
    PISOP32A32_DIOB = IXPIO_DIO_B
except:
    pass

# /usr/ixpio/include/piodio.h: 141
try:
    PISOP32A32_DIOC = IXPIO_DIO_C
except:
    pass

# /usr/ixpio/include/piodio.h: 142
try:
    PISOP32A32_DIOD = IXPIO_DIO_D
except:
    pass

# /usr/ixpio/include/piodio.h: 143
try:
    PISOP32A32_DIO_ALL = IXPIO_DIO
except:
    pass

port_list = struct_port_list # /usr/ixpio/include/piodio.h: 150

port_config = struct_port_config # /usr/ixpio/include/piodio.h: 159

dev_control = struct_dev_control # /usr/ixpio/include/piodio.h: 176

# No inserted files

