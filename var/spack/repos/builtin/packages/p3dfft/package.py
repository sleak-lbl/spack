# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install p3dfft
#
# You can edit this file again by typing:
#
#     spack edit p3dfft
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class P3dfft(AutotoolsPackage):
    """P3DFFT: Scalable Framework for Three-Dimensional Fourier Transforms."""

    homepage = "https://www.p3dfft.net/"
    url      = "https://github.com/sdsc/p3dfft/archive/2.7.9.tar.gz"

    version('2.7.9', sha256='c61b4705be59f20f06ef2fa11971f3648f82560c1078311c464c12f581b36ed1')
    version('2.7.8', sha256='e54588d922b3d7f31aad16a95c393474e5e83c08affcfd7a5792830c92ea4013')
    version('2.7.7', sha256='33ea9683f863bda40d15a8cc9dba2f01b6aef4f2c4b39665889cf1225291dca1')

    depends_on('fftw')
    depends_on('mpi')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('HUGETLB_VERBOSE', 0)

    def configure_args(self):
        args = ['FC=ftn', 'CC=cc']
        if self.spec.compiler.name == 'intel':
            args.append('--enable-intel')
        elif self.spec.compiler.name == 'gcc':
            args.append('--enable-gnu')
        elif self.spec.compiler.name == 'cce':
            args.append('--enable-cray')
        else:
            args.append('--enable-intel')
        args.append('--enable-fftw')
        args.append('--with-fftw='+self.spec['fftw'].prefix)
        return args
