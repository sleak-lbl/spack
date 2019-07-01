# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Adios(AutotoolsPackage):
    """The Adaptable IO System (ADIOS) provides a simple,
    flexible way for scientists to describe the
    data in their code that may need to be written,
    read, or processed outside of the running simulation.
    """

    homepage = "http://www.olcf.ornl.gov/center-projects/adios/"
    url      = "https://github.com/ornladios/ADIOS/archive/v1.12.0.tar.gz"
    git      = "https://github.com/ornladios/ADIOS.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('1.13.1', '958aed11240d7f5a065ab5ee271ecb44')
    version('1.13.0', '68af36b821debbdf4748b20320a990ce')
    version('1.12.0', '84a1c71b6698009224f6f748c5257fc9')
    version('1.11.1', '5639bfc235e50bf17ba9dafb14ea4185')
    version('1.11.0', '5eead5b2ccf962f5e6d5f254d29d5238')
    version('1.10.0', 'eff450a4c0130479417cfd63186957f3')
    version('1.9.0',  '310ff02388bbaa2b1c1710ee970b5678')

    variant('shared', default=True,
            description='Builds a shared version of the library')

    variant('fortran', default=False,
            description='Enable Fortran bindings support')

    variant('mpi', default=True,
            description='Enable MPI support')
    variant('infiniband', default=False,
            description='Enable infiniband support')

    # transforms
    variant('zlib', default=True,
            description='Enable zlib transform support')
    variant('bzip2', default=False,
            description='Enable bzip2 transform support')
    variant('szip', default=False,
            description='Enable szip transform support')
    variant('zfp', default=True,
            description='Enable ZFP transform support')
    variant('sz', default=True,
            description='Enable SZ transform support')
    variant('lz4', default=True,
            description='Enable LZ4 transform support')
    variant('blosc', default=True,
            description='Enable Blosc transform support')
    # transports and serial file converters
    variant('hdf5', default=False,
            description='Enable parallel HDF5 transport and serial bp2h5 ' +
                        'converter')
    variant('netcdf', default=False, description='Enable netcdf support')

    variant(
        'staging', values=any_combination_of('flexpath', 'dataspaces'),
        description='Enable dataspaces and/or flexpath staging transports'
    )

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool@:2.4.2', type='build')
    depends_on('python', type='build')

    depends_on('mpi', when='+mpi')
    # optional transformations
    depends_on('zlib', when='+zlib')
    depends_on('bzip2', when='+bzip2')
    depends_on('szip', when='+szip')
    depends_on('sz@:1.4.10', when='@:1.12.0 +sz')
    depends_on('sz@1.4.11.0:1.4.11.99', when='@1.13.0 +sz')
    depends_on('sz@1.4.12.3:1.4.12.99', when='@1.13.1: +sz')
    depends_on('zfp@:0.5.0', when='+zfp')
    depends_on('lz4', when='+lz4')
    depends_on('c-blosc@1.12.0:', when='+blosc')
    # optional transports & file converters
    depends_on('hdf5@1.8:+hl+mpi', when='+hdf5')
    depends_on('netcdf', when='+netcdf')
    depends_on('libevpath', when='staging=flexpath')
    depends_on('dataspaces+mpi', when='staging=dataspaces')

    for p in ['+hdf5', '+netcdf', 'staging=flexpath', 'staging=dataspaces']:
        conflicts(p, when='~mpi')

    build_directory = 'spack-build'

    # ADIOS uses the absolute Python path, which is too long and results in
    # "bad interpreter" errors - but not applicable for 1.9.0
    patch('python.patch', when='@1.10.0:')
    # Fix ADIOS <=1.10.0 compile error on HDF5 1.10+
    #   https://github.com/ornladios/ADIOS/commit/3b21a8a41509
    #   https://github.com/spack/spack/issues/1683
    patch('adios_1100.patch', when='@:1.10.0^hdf5@1.10:')

    def validate(self, spec):
        """Checks if incompatible variants have been activated at the same time

        Args:
            spec: spec of the package

        Raises:
            RuntimeError: in case of inconsistencies
        """
        if '+fortran' in spec and not self.compiler.fc:
            msg = 'cannot build a fortran variant without a fortran compiler'
            raise RuntimeError(msg)

    def with_or_without_hdf5(self, activated):

        if activated:
            return '--with-phdf5={0}'.format(
                self.spec['hdf5'].prefix
            )

        return '--without-phdf5'

    def configure_args(self):
        spec = self.spec
        self.validate(spec)

        extra_args = [
            # required, otherwise building its python bindings will fail
            'CFLAGS={0}'.format(self.compiler.pic_flag)
        ]

        extra_args += self.enable_or_disable('shared')
        extra_args += self.enable_or_disable('fortran')

        if '+mpi' in spec:
            env['MPICC'] = spec['mpi'].mpicc
            env['MPICXX'] = spec['mpi'].mpicxx

        extra_args += self.with_or_without('mpi', activation_value='prefix')
        extra_args += self.with_or_without('infiniband')

        # Transforms
        variants = ['zlib', 'bzip2', 'szip']
        if spec.satisfies('@1.11.0:'):
            variants += ['zfp']
        if spec.satisfies('@1.12.0:'):
            variants += ['sz', 'lz4']
        if spec.satisfies('@1.13.0:'):
            extra_args += self.with_or_without(
                'blosc',
                activation_value=lambda x: spec['c-blosc'].prefix
            )

        # External I/O libraries
        variants += ['hdf5', 'netcdf']

        for x in variants:
            extra_args += self.with_or_without(x, activation_value='prefix')

        # Staging transports
        def with_staging(name):
            if name == 'flexpath':
                return spec['libevpath'].prefix
            return spec[name].prefix

        extra_args += self.with_or_without(
            'staging',
            activation_value=with_staging
        )

        # Staging transports
        if "+flexpath" in spec or "+staging" in spec:
            extra_args.append("--with-flexpath=%s" % spec["libevpath"].prefix)
        else:
            extra_args.append("--without-flexpath")

        if "+dataspaces" in spec or "+staging" in spec:
            extra_args.append("--with-dataspaces=%s" % spec["dataspaces"].prefix)
        else:
            extra_args.append("--without-dataspaces")
        return extra_args
