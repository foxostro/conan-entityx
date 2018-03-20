from conans import ConanFile, CMake


class EntityxConan(ConanFile):
    name = "EntityX"
    author = "Alec Thomas <alec@swapoff.org>"
    version = "1.2.0"
    license = "MIT"
    description = """Entity Component Systems (ECS) are a form of decomposition that completely decouples entity logic and data from the entity "objects" themselves. The Evolve your Hierarchy article provides a solid overview of EC systems and why you should use them.

EntityX is an EC system that uses C++11 features to provide type-safe component management, event delivery, etc. It was built during the creation of a 2D space shooter.
    """
    url = "https://github.com/foxostro/conan-entityx"
    settings = "os", "compiler", "build_type", "arch"
    options = {"benchmarks": [True, False],
               "max_components": "ANY",
               "shared": [True, False],
               "testing": [True, False],
               "dt_type": "ANY"
               }
    default_options = "benchmarks=True", "max_components=64", "shared=False", "testing=True", "dt_type=double"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/alecthomas/entityx.git --branch {version} --depth 1".format(version=self.version))
        self.run("sed -ibak s/-Werror// entityx/CMakeLists.txt")

    def build(self):
        cmake = CMake(self)
        args = []
        args += ["-DENTITYX_RUN_BENCHMARKS={}".format("1" if self.options.benchmarks else "0")]
        args += ["-DENTITYX_MAX_COMPONENTS={}".format(self.options.max_components)]
        args += ["-DENTITYX_BUILD_SHARED={}".format("1" if self.options.shared else "0")]
        args += ["-DENTITYX_BUILD_TESTING={}".format("1" if self.options.testing else "0")]
        args += ["-DENTITYX_DT_TYPE={}".format(self.options.dt_type)]

        self.run("cmake entityx {cmd} {args}".format(cmd=cmake.command_line, args=" ".join(args)))
        self.run("cmake --build . {config}".format(config=cmake.build_config))

    def package(self):
        self.copy('*.h', dst='include/entityx', src='entityx/entityx')
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["entityx"]
