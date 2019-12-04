# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

# typical working line with extrae 3.0.1
# ./configure
#   --prefix=/usr/local
#   --with-mpi=/usr/lib64/mpi/gcc/openmpi
#   --with-unwind=/usr/local
#   --with-papi=/usr
#   --with-dwarf=/usr
#   --with-elf=/usr
#   --with-dyninst=/usr
#   --with-binutils=/usr
#   --with-xml-prefix=/usr
#   --enable-openmp
#   --enable-nanos
#   --enable-pthread
#   --disable-parallel-merge
#
# LDFLAGS=-pthread


class Extrae(AutotoolsPackage):
    """Extrae is the package devoted to generate tracefiles which can
       be analyzed later by Paraver. Extrae is a tool that uses
       different interposition mechanisms to inject probes into the
       target application so as to gather information regarding the
       application performance. The Extrae instrumentation package can
       instrument the MPI programin model, and the following parallel
       programming models either alone or in conjunction with MPI :
       OpenMP, CUDA, OpenCL, pthread, OmpSs"""
    homepage = "https://tools.bsc.es/extrae"
    url      = "https://ftp.tools.bsc.es/extrae/extrae-3.4.1-src.tar.bz2"
    version('3.7.1', sha256='95810b057f95e91bfc89813eb8bd320dfe40614fc8e98c63d95c5101c56dd213')
    version('3.7.0', sha256='1baf31bb83e44cba600a0a947634a95b8d459518fc698bebfa5816522f5d1be6')
    version('3.6.1', sha256='c44d73283251c5141a9898b9af025a626bef753da3f70527f8f237a29b468bd5')
    version('3.6.0', sha256='48a5210b8eab3a11d26c508ab9c627ec80a28dd35299d77cf6c9a1a70822f31c')
    version('3.5.4', sha256='e767397f56c36b89dcc789c78404716597444f6633763449916738d85589b1f0')
    version('3.5.2', sha256='3476fab30747d675920a318bf0c00da8a10094b52aeb0f691b796a580a694893')
    version('3.5.1', sha256='367b7674b85a0c59b32eb54a6c836274b11912ecfce9d7bdc39ffceaa439d898')
    version('3.5.0', sha256='e78446ab96af90cc80932bc77e13cc86b2cc81bc9c2bbef3d806e79dc45b9208')
    version('3.4.3', sha256='feede830f6058e0e262d27b6452b545100498f7648c38a4f15de77bb4df4de01')
    version('3.4.1', '69001f5cfac46e445d61eeb567bc8844')

    depends_on("autoconf", type='build')
    depends_on("automake", type='build')
    depends_on("libtool", type='build')
    depends_on("m4", type='build')
    depends_on("mpi")
    depends_on("libunwind")
    depends_on("boost")
    depends_on("libdwarf")
    depends_on("papi")
    depends_on("elf", type="link")
    depends_on("libxml2")
    depends_on("numactl")
    depends_on("binutils+libiberty")
    depends_on("gettext")
    # gettext dependency added to find -lintl
    # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined

    build_directory = 'spack-build'

    variant('dyninst', default=False, description="Use dyninst for dynamic code installation")
    depends_on('dyninst@:9', when='+dyninst')

    variant('papi', default=True, description="Use PAPI to collect performance counters")
    depends_on('papi', when='+papi')

    def configure_args(self):
        spec = self.spec
        args = ["--with-mpi=%s" % spec['mpi'].prefix,
                "--with-unwind=%s" % spec['libunwind'].prefix,
                "--with-boost=%s" % spec['boost'].prefix,
                "--with-dwarf=%s" % spec['libdwarf'].prefix,
                "--with-elf=%s" % spec['elf'].prefix,
                "--with-xml-prefix=%s" % spec['libxml2'].prefix,
                "--with-binutils=%s" % spec['binutils'].prefix]

        args += (["--with-papi=%s" % spec['papi'].prefix]
                 if '+papi' in self.spec else
                 ["--without-papi"])

        args += (["--with-dyninst=%s" % spec['dyninst'].prefix]
                 if '+dyninst' in self.spec else
                 ["--without-dyninst"])

        if spec.satisfies("^dyninst@9.3.0:"):
            make.add_default_arg("CXXFLAGS=%s" % self.compiler.cxx11_flag)
            args.append("CXXFLAGS=%s" % self.compiler.cxx11_flag)

        # This was added due to configure failure
        # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
        args.append('LDFLAGS=-lintl')

        return(args)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            # parallel installs are buggy prior to 3.7
            # see https://github.com/bsc-performance-tools/extrae/issues/18
            if(spec.satisfies('@3.7:')):
                make('install', parallel=True)
            else:
                make('install', parallel=False)

    def setup_run_environment(self, env):
        # set EXTRAE_HOME in the module file
        env.set('EXTRAE_HOME', self.prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # set EXTRAE_HOME for everyone using the Extrae package
        env.set('EXTRAE_HOME', self.prefix)
