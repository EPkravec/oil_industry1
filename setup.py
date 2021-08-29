#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "1.1.20.0"

import atexit
from os.path import join, dirname
from traceback import format_exc

from setuptools import setup, find_packages
from setuptools.command.install import install

xp = []
zs = False


class CustomInstall(install):
    global xp, zs

    def run(self):

        print("HELLO!")
        # print dirname(__file__)

        packages = find_packages()

        def _post_install():
            import os.path, re

            print("POST INSTALL STEPS")

            def find_modules_path():
                import sys

                return ['/usr/local/lib/python%s.%s/dist-packages/%s' % (
                    sys.version_info[0], sys.version_info[1], packages[0])]

                for p in sys.path:
                    if re.search('/python[0-9.]+/', p):
                        for my_name in packages:
                            if os.path.isdir(p) and my_name in os.listdir(p):
                                z = os.path.join(p, my_name)
                                if len(z) > 10:
                                    xp.append(z)
                                    if re.search(r'/usr/local/.*/dist-packages', p):
                                        zs = z
                if zs:
                    xp.insert(0, zs)

                return xp

            install_paths = find_modules_path()

            print("INSTALL PATHS:%s" % install_paths)

            pyc_files = []
            py_files = []

            bsf = '#/bin/bash\n'
            for ip in install_paths:

                for root, dirnames, filenames in os.walk(ip):

                    for filename in filenames:
                        if filename.endswith('.pyc'):
                            pyc_files.append(os.path.join(root, filename))
                        elif filename.endswith('.py'):
                            py_files.append(os.path.join(root, filename))

                for py_file in py_files:
                    if py_file + 'c' in pyc_files:
                        if not re.search('/kiosk_', py_file):

                            try:
                                bsf += 'rm -f %s\n' % py_file
                                os.remove(py_file)
                            except:
                                pass

            try:
                os.mkdir('/var/kiosk', 0o755)
            except:
                pass
            try:
                os.mkdir('/var/kiosk/clean.d', 0o755)
            except:
                pass

            sern = packages[0]
            fn = '/var/kiosk/clean.d/%s.sh' % sern
            bsf += "rm -f %s\n" % fn
            f = open(fn, 'w')
            f.write(bsf)
            f.close()
            os.chmod(fn, 0o755)

            try:
                stmp = dirname(__file__) + '/service_template.sh'
                t = open(stmp, 'r').read()
                t = t.replace('<USERNAME>', 'root')
                fid = install_paths[0] + '/server.pyc'
                t = t.replace('<COMMAND>', 'python %s' % fid)
                t = t.replace('<FID>', fid)
                t = t.replace('<DIR>', install_paths[0])
                sern = packages[0]
                t = t.replace('<NAME>', sern)
                t = t.replace('<DESCRIPTION>', '%s deamon ver %s' % (sern, __version__))

                t = t.replace('<TCP_PORT>', '7000')  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!

                fn = '/etc/init.d/%s' % sern
                f = open(fn, 'w')
                f.write(t)
                f.close()
                os.chmod(fn, 0o755)

                import subprocess
                bsc = [
                    'update-rc.d "%s" defaults' % sern,
                    'service %s stop' % sern,
                    'service %s start' % sern,
                ]
                for bashCommand in bsc:
                    print(bashCommand)
                    os.system(bashCommand)
            except:
                f = open("/var/log/setup-err", "w")
                f.write(format_exc())
                f.close()

            print("BYE!")

        atexit.register(_post_install)
        install.run(self)


setup(
    cmdclass={'install': CustomInstall},
    name='oil_industry',
    version=__version__,
    description='new projecktion',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='k.e.p',
    author_email='kravec.egor@gmail.com',
    license='BSD',
    install_requires=open(join(dirname(__file__), 'requirements.txt')).read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='oil_industry',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]

)
