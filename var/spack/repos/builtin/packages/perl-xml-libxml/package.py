# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only

from spack import *


class PerlXmlLibxml(PerlPackage):
    """This module is an interface to libxml2, providing XML and HTML parsers
       with DOM, SAX and XMLReader interfaces"""

    homepage = "http://search.cpan.org/~shlomif/XML-LibXML-2.0132/LibXML.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/XML-LibXML-2.0132.tar.gz"

    version('2.0132', '43546fd9a3974f19323f9fb04861ece9')
