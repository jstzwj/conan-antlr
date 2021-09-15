from conans import ConanFile, CMake, tools
import os


class Antlr4Conan(ConanFile):
    name = "antlr4"
    version = "4.9.2"

    # Optional metadata
    license = "The BSD 3-clause license"
    author = "Terence Parr <parrt@cs.usfca.edu>"
    url = "https://github.com/antlr/antlr4/tree/master/runtime/Cpp"
    description = "C++ target for ANTLR 4"
    topics = ("parser", "compiler")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "static_crt": [True, False]}
    default_options = {"shared": False, "static_crt": False}

    def source(self):
        source_url = "https://www.antlr.org/download/antlr4-cpp-runtime-{}-source.zip".format(self.version)
        tools.get(source_url, sha256="838a2c804573f927c044e5f45a8feb297683a7047ab62dfac8ddc995498db11c")
        source_url2 = "https://www.antlr.org/download/antlr-{}-complete.jar".format(self.version)
        antlr_file_name = "antlr.jar"
        tools.download(source_url2, antlr_file_name)
        tools.check_sha256(antlr_file_name, "bb117b1476691dc2915a318efd36f8957c0ad93447fb1dac01107eb15fe137cd")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["WITH_LIBCXX"]="ON" if self.options['shared'] else "OFF"
        cmake.definitions["WITH_STATIC_CRT"]="ON" if self.options['static_crt'] else "OFF"
        cmake.definitions["WITH_DEMO"]="ON"
        cmake.definitions["ANTLR_JAR_LOCATION"]="antlr.jar"
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build(target='antlr4_static')

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self.source_folder, "runtime", "src"))
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.jar", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)