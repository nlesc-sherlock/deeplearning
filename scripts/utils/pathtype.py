# patharg.py
# Blatantly stolen from https://mail.python.org/pipermail/stdlib-sig/2015-July/000990.html
from argparse import ArgumentTypeError
import os

class PathType(object):
    def __init__(self, exists=True, type='file', dash_ok=True, abs=False):
        '''exists:
                True: a path that does exist
                False: a path that does not exist, in a valid parent directory
                None: don't care, in a valid parent directory
           type: file, dir, symlink, None, or a function returning True for valid paths
                None: don't care
           dash_ok: whether to allow - as stdin/stdout
           abs: if True, path will be coerced to an absolute path'''

        assert exists in (True, False, None)
        assert type in ('file','dir','symlink',None) or hasattr(type,'__call__')

        self._exists = exists
        self._type = type
        self._dash_ok = dash_ok

    def __call__(self, string):
        if string=='-':
            # the special argument "-" means sys.std{in,out}
            if self._type == 'dir':
                raise ArgumentTypeError('standard input/output (-) not allowed as directory path')
            elif self._type == 'symlink':
                raise ArgumentTypeError('standard input/output (-) not allowed as symlink path')
            elif not self._dash_ok:
                raise ArgumentTypeError('standard input/output (-) not allowed')
        else:
            np = os.path.abspath(string) if abs else os.path.normpath(string)
            e = os.path.exists(np)
            if self._exists==True:
                if not e:
                    raise ArgumentTypeError("path does not exist: '%s'" % np)

                if self._type is None:
                    pass
                elif self._type=='file':
                    if not os.path.isfile(np):
                        raise ArgumentTypeError("path is not a file: '%s'" % np)
                elif self._type=='symlink':
                    if not os.path.symlink(np):
                        raise ArgumentTypeError("path is not a symlink: '%s'" % np)
                elif self._type=='dir':
                    if not os.path.isdir(np):
                        raise ArgumentTypeError("path is not a directory: '%s'" % np)
                elif not self._type(np):
                    raise ArgumentTypeError("path not valid: '%s'" % np)
            else:
                if self._exists==False and e:
                    raise ArgumentTypeError("path exists: '%s'" % np)

                p = os.path.dirname(os.path.normpath(np)) or '.'
                if not os.path.isdir(p):
                    raise ArgumentTypeError("parent path is not a directory: '%s'" % p)
                elif not os.path.exists(p):
                    raise ArgumentTypeError("parent directory does not exist: '%s'" % p)

        return np