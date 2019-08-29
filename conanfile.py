import glob
import os

from conans import CMake, ConanFile, tools


class RapidCheck(ConanFile):
    name = "rapidcheck"
    version = "20190829"
    description = "QuickCheck clone for C++ with the goal of being simple to use with as little boilerplate as possible."
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = "testing"
    url = "https://github.com/rhololkeolke/conan-rapidcheck"
    homepage = "https://github.com/emil-e/rapidcheck/"
    author = "Devin Schwab <dschwab@andrew.cmu.edu>"
    license = (
        "BSD-2-Clause"
    )  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]  # Packages the license for the
    exports_sources = ["CMakeLists.txt"]
    # conanfile.py
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git(folder=self._source_subfolder)
        git.clone("https://github.com/emil-e/rapidcheck.git", branch="master")
        git.checkout("d598a058cb275f7704f0a8b1fe31eb75b1710934")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
