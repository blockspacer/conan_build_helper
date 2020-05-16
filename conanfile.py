from conans import ConanFile
from conan_build_helper.cmake import *
from conan_build_helper.headeronly import *
from conan_build_helper.require_scm import *

class ConanCommonRecipes(ConanFile):
    name = "conan_build_helper"
    version = "0.0.1"
    url = "https://gitlab.com/USERNAME/conan_build_helper"
    license = "MIT"
    description = "Common recipes for conan.io packages"
    exports = "*.py"
