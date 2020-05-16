from conans import ConanFile, python_requires

common = python_requires('conan_build_helper/0.0.1@conan/stable')

class ConanCommonRecipesTest(common.HeaderOnlyPackage):
    def test(self):
        pass
