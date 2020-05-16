from conans import ConanFile
from conans import CMake
from conans import tools
from conans.tools import collect_libs
from conans.tools import OSInfo
from conan_build_helper.headeronly import package_headers
from conan_build_helper.require_scm import RequireScm
import os
import traceback
import shutil

# if you using python less than 3 use from distutils import strtobool
from distutils.util import strtobool

# conan runs the methods in this order:
# config_options(),
# configure(),
# requirements(),
# package_id(),
# build_requirements(),
# build_id(),
# system_requirements(),
# source(),
# imports(),
# build(),
# package(),
# package_info()

class CMakePackage(ConanFile, RequireScm):
    def _verbose_makefile(self):
        return os.environ.get('CONAN_' + self.name.upper() + '_VERBOSE_MAKEFILE') is not None

    def _cmake_defs_from_options(self):
        defs = {}

        for name, value in self.options.values.as_list():
            defs[(self.name.upper() + '_' + name.upper()).replace('-', '_')] = value

        defs['CMAKE_VERBOSE_MAKEFILE'] = True

        if 'shared' in self.options:
            defs['CMAKE_BUILD_SHARED_LIBS'] = self.options.shared

        return defs

    # build-only option
    # see https://github.com/conan-io/conan/issues/6967
    # conan ignores changes in environ, so
    # use `conan remove` if you want to rebuild package
    def _environ_option(self, name, default = 'true'):
      env_val = default.lower() # default, must be lowercase!
      # allow both lowercase and uppercase
      if name.upper() in os.environ:
        env_val = os.getenv(name.upper())
      elif name.lower() in os.environ:
        env_val = os.getenv(name.lower())
      # strtobool:
      #   True values are y, yes, t, true, on and 1;
      #   False values are n, no, f, false, off and 0.
      #   Raises ValueError if val is anything else.
      #   see https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool
      return bool(strtobool(env_val))

    def _is_tests_enabled(self):
      return self._environ_option("ENABLE_TESTS", default = 'true')

    def add_cmake_option(var_name, value):
        value_str = "{}".format(value)
        var_value = "ON" if bool(strtobool(value_str.lower())) else "OFF"
        self.output.info('added cmake definition %s = %s' % (var_name, var_value))
        cmake.definitions[var_name] = var_value

    @property
    def _custom_cmake_defs(self):
        return getattr(self, 'custom_cmake_defs', {})

    def _parallel_build(self):
        return os.environ.get('CONAN_' + self.name.upper() + '_SINGLE_THREAD_BUILD') is None

    def build(self):
        cmake = CMake(self, parallel=self._parallel_build())
        cmake.configure(defs={**self._cmake_defs_from_options(), **self._custom_cmake_defs}, source_folder=self._repository_path)
        cmake.build()
        cmake.install()

    def package(self):
        package_headers(self)
        self.copy('*.a', dst='lib', keep_path=False)
        self.copy('*.so', dst='lib', keep_path=False)
        self.copy('*.lib', dst='lib', keep_path=False)
        self.copy('*.dll', dst='lib', keep_path=False)

    def package_info(self):
        self.output.info("Collecting package libs...")
        self.cpp_info.libs = collect_libs(self)

