# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.

from spack import *
from spack.util.prefix import Prefix
import os
import platform

# FIXME Remove hack for polymorphic versions
# This package uses a ugly hack to be able to dispatch, given the same
# version, to different binary packages based on the platform that is
# running spack. See #13827 for context.
# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()
_versions = {
    '20.9': {
        'Linux-aarch64': ('3bfb3d17f5ee99998bcc30d738e818d3b94b828e2d8da7db48bf152a01e22023', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_aarch64_cuda_11.0.tar.gz'),
        'Linux-ppc64le': ('b2966d4047e1dfd981ce63b333ab9c0acbdc2a6a505fa217456ac9fa3b8e7474', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('fe665ab611b03846a90bd70ca4e08c1e59ab527364b971ed0304e0ae73c778d8', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_x86_64_cuda_multi.tar.gz')},
    '20.7': {
        'Linux-aarch64': ('5b83ca1919199ac0aa609309b31c345c5a6453dd3131fddeef9e3ee9059a0e9b', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_aarch64_cuda_11.0.tar.gz'),
        'Linux-ppc64le': ('800ead240bdf61611910b2f6df24ee1d7359377ff3767c923738dd81fcea9312', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('a5c5c8726d2210f2310a852c6d6e03c9ef8c75e3643e9c94e24909f5e9c2ea7a', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz')}
}


class Nvhpc(Package):
    """The NVIDIA HPC SDK is a comprehensive suite of compilers, libraries
    and tools essential to maximizing developer productivity and the
    performance and portability of HPC applications. The NVIDIA HPC
    SDK C, C++, and Fortran compilers support GPU acceleration of HPC
    modeling and simulation applications with standard C++ and
    Fortran, OpenACC directives, and CUDA. GPU-accelerated math
    libraries maximize performance on common HPC algorithms, and
    optimized communications libraries enable standards-based
    multi-GPU and scalable systems programming. Performance profiling
    and debugging tools simplify porting and optimization of HPC
    applications."""

    homepage = "http://developer.nvidia.com/hpc-sdk"

    maintainers = ['samcmill']

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    variant('blas',         default=True,
            description="Enable BLAS")
    variant('install_type', default='single',
            values=('single', 'network'), multi=False,
            description='Network installs are for installations shared '
                        'by different operating systems')
    variant('lapack',       default=True,
            description="Enable LAPACK")
    variant('mpi',          default=False,
            description="Enable MPI")

    provides('blas',        when='+blas')
    provides('lapack',      when='+lapack')
    provides('mpi',         when='+mpi')

    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['NVHPC_SILENT'] = "true"
        os.environ['NVHPC_ACCEPT_EULA'] = "accept"
        os.environ['NVHPC_INSTALL_DIR'] = prefix

        if spec.variants['install_type'].value == 'network':
            os.environ['NVHPC_INSTALL_TYPE'] = "network"
            os.environ['NVHPC_INSTALL_LOCAL_DIR'] = \
                "%s/%s/%s/share_objects" % \
                (prefix, 'Linux_%s' % spec.target.family, self.version)
        else:
            os.environ['NVHPC_INSTALL_TYPE'] = "single"

        # Run install script
        os.system("./install")

    def setup_run_environment(self, env):
        prefix = Prefix(join_path(self.prefix,
                                  'Linux_%s' % self.spec.target.family,
                                  self.version, 'compilers'))

        env.set('CC',  join_path(prefix.bin, 'nvc'))
        env.set('CXX', join_path(prefix.bin, 'nvc++'))
        env.set('F77', join_path(prefix.bin, 'nvfortran'))
        env.set('FC',  join_path(prefix.bin, 'nvfortran'))

        env.prepend_path('PATH',            prefix.bin)
        env.prepend_path('CPATH',           prefix.include)
        env.prepend_path('LIBRARY_PATH',    prefix.lib)
        env.prepend_path('LD_LIBRARY_PATH', prefix.lib)
        env.prepend_path('MANPATH',         prefix.man)

        if '+mpi' in self.spec:
            mpi_prefix = Prefix(join_path(self.prefix,
                                          'Linux_%s' % self.spec.target.family,
                                          self.version, 'comm_libs', 'mpi'))
            env.prepend_path('PATH', mpi_prefix.bin)
            env.prepend_path('CPATH', mpi_prefix.include)
            env.prepend_path('LD_LIBRARY_PATH', mpi_prefix.lib)

    def setup_dependent_package(self, module, dependent_spec):
        if '+mpi' in self.spec or self.provides('mpi'):
            mpi_prefix = Prefix(join_path(self.prefix,
                                          'Linux_%s' % self.spec.target.family,
                                          self.version, 'comm_libs', 'mpi'))

            self.spec.mpicc  = join_path(mpi_prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(mpi_prefix.bin, 'mpicxx')
            self.spec.mpif77 = join_path(mpi_prefix.bin, 'mpif77')
            self.spec.mpifc  = join_path(mpi_prefix.bin, 'mpif90')

    @property
    def libs(self):
        prefix = Prefix(join_path(self.prefix,
                                  'Linux_%s' % self.spec.target.family,
                                  self.version, 'compilers'))
        libs = []

        if '+blas' in self.spec:
            libs.append('libblas')

        if '+lapack' in self.spec:
            libs.append('liblapack')
            libs.append('libnvf')

        return find_libraries(libs, root=prefix, recursive=True)
