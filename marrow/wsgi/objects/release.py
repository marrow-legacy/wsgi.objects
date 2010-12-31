# encoding: utf-8

"""Release information about Marrow WSGI Objects."""


__all__ = ['version_info', 'version', 'release']



version_info = (0, 1, 0, 'alpha')
version = '.'.join(str(n) for n in version_info[:3])
release = version + ''.join(str(n) for n in version_info[3:])
