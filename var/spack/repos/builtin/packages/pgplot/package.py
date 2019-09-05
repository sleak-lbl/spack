# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pgplot(Package):
    """The PGPLOT Graphics Subroutine Library is a Fortran- or C-callable,
    device-independent graphics package for making simple scientific graphs. It is
    intended for making graphical images of publication quality with minimum effort
    on the part of the user. For most applications, the program can be
    device-independent, and the output can be directed to the appropriate device at
    run time."""

    homepage = "http://www.astro.caltech.edu/~tjp/pgplot/"
    url      = "ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot5.2.tar.gz"

    version('5.2', 'a5799ff719a510d84d26df4ae7409ae61fe66477e3f1e8820422a9a4727a5be4')

    patch('drivers.list.patch', level=0) # Enable drivers requested by NERSC users.
    patch('g77_gcc.patch', level=0) # Rename g77 to gfotran for compilation.

    parallel = False

    # pgplot will likely be run only on eLogins, which do not support Cray
    # hugepages.
    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        spack.util.module_cmd.module('unload', 'craype-hugepages2M')

    def install(self, spec, prefix):
        configure = Executable('./makemake . linux g77_gcc')
        configure()
        make()

	# pgplot creates a few libs and a few misc files, but the makefile that
	# it generates has no 'install' target, so we have to copy the files to
	# the install dir manually.
        mkdirp(prefix.lib)
        files_to_install = ['grfont.dat', 'libpgplot.a', 'libpgplot.so',
                            'pgxwin_server', 'rgb.txt']
        for f in files_to_install:
          install(f, prefix.lib)
