# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libiconv(AutotoolsPackage):
    """GNU libiconv provides an implementation of the iconv() function
    and the iconv program for character set conversion."""

    homepage = "https://www.gnu.org/software/libiconv/"
    url      = "https://ftpmirror.gnu.org/libiconv/libiconv-1.15.tar.gz"

    version('1.15', 'ace8b5f2db42f7b3b3057585e80d9808')
    version('1.14', 'e34509b1623cec449dfeb73d7ce9c6c6')

    variant('static', default=False, description='also build a static library')


    # We cannot set up a warning for gets(), since gets() is not part
    # of C11 any more and thus might not exist.
    patch('gets.patch', when='@1.14')

    conflicts('@1.14', when='%gcc@5:')

    def configure_args(self):
        args = ['--enable-extra-encodings']
        if '+static' in self.spec:
            args += ['--enable-static']

        # A hack to patch config.guess in the libcharset sub directory
        copy('./build-aux/config.guess',
             'libcharset/build-aux/config.guess')
        return args

#    # is this how you get a thing that uses this package to add "-liconv" to its link flags?
#    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
#        spack_env.set('LDFLAGS', '-liconv') 
