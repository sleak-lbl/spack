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
#     spack install arm-reports
#
# You can edit this file again by typing:
#
#     spack edit arm-reports
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os


class ArmReports(Package):
    """Arm Performance Reports is a low-overhead tool that produces
    one-page text and HTML reports summarizing and characterizing both
    scalar and MPI application performance."""

    homepage = "http://www.allinea.com/products/allinea-performance-reports"

    # TODO: this mess should be fixed as soon as a way to parametrize/constrain
    #       versions (and checksums) based on the target platform shows up

    version(
        "19.1.1-Suse-15-x86_64",
        sha256="5b680c7332592d6347c5ce6ffd9df7f1e67faecf65aa5cd9ddb3ccc2e7ed530c",
        url="http://content.allinea.com/downloads/arm-reports-19.1.1-Suse-15.0-x86_64.tar",
    )
    version(
        "19.1-Suse-15-x86_64",
        sha256="bf0c1b7623f9ac905e21eac26c3aee1c9ecdbdcdbaed48995fc9e3c1dec6942b",
        url="http://content.allinea.com/downloads/arm-reports-19.1-Suse-15.0-x86_64.tar",
    )
    version(
        "19.0.5-Suse-15-x86_64",
        sha256="e67f5194525e80bb989c20b7385c3f30c3383c4fcee5799bbaa44cee731cef63",
        url="http://content.allinea.com/downloads/arm-reports-19.0.5-Suse-15.0-x86_64.tar",
    )

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["licences/Licence"]
    license_vars = [
        "ALLINEA_LICENSE_DIR",
        "ALLINEA_LICENCE_DIR",
        "ALLINEA_LICENSE_FILE",
        "ALLINEA_LICENCE_FILE",
    ]
    #license_url = "http://www.allinea.com/user-guide/forge/Installation.html"
    license_url = "https://developer.arm.com/docs/101169/latest/using-arm-licence-server"

    def install(self, spec, prefix):
        os.system("./textinstall.sh --accept-licence " + prefix)
