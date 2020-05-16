from conans import ConanFile
from conan_build_helper.require_scm import RequireScm
import os

def package_headers(conanfile):
        include_dir = conanfile._repository_include_dir_required

        for ext in ['*.h', '*.hpp', '*.hxx', '*.hcc']:
            conanfile.copy(ext, dst='include', src=include_dir)

class HeaderOnlyPackage(ConanFile, RequireScm):
    def package(self):
        package_headers(self)

    def package_id(self):
        self.info.header_only()
