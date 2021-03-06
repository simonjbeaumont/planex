# Run these tests with 'nosetests':
#   install the 'python-nose' package (Fedora/CentOS or Ubuntu)
#   run 'nosetests' in the root of the repository

import unittest
import platform
import planex.spec


def get_rpm_machine():
    if platform.machine() == 'x86_64':
        return 'x86_64'
    return 'i386'


def get_deb_machine():
    if platform.machine() == 'x86_64':
        return 'amd64'
    return 'i386'


class RpmTests(unittest.TestCase):
    def setUp(self):
        # 'setUp' breaks Pylint's naming rules
        # pylint: disable=C0103
        self.spec = planex.spec.Spec("tests/data/ocaml-cohttp.spec",
                                     dist=".el6")

    def test_good_filename_preprocessor(self):
        planex.spec.Spec("tests/data/ocaml-cohttp.spec.in")

    def test_bad_filename(self):
        self.assertRaises(planex.spec.SpecNameMismatch, planex.spec.Spec,
                          "tests/data/bad-name.spec")

    def test_bad_filename_preprocessor(self):
        self.assertRaises(planex.spec.SpecNameMismatch, planex.spec.Spec,
                          "tests/data/bad-name.spec.in")

    def test_name(self):
        self.assertEqual(self.spec.name(), "ocaml-cohttp")

    def test_specpath(self):
        self.assertEqual(self.spec.specpath(), "./SPECS/ocaml-cohttp.spec")

    def test_version(self):
        self.assertEqual(self.spec.version(), "0.9.8")

    def test_provides(self):
        self.assertEqual(
            self.spec.provides(),
            set(["ocaml-cohttp", "ocaml-cohttp-devel"]))

    def test_source_urls(self):
        self.assertEqual(
            self.spec.source_urls(),
            ["https://github.com/mirage/ocaml-cohttp/archive/"
             "ocaml-cohttp-0.9.8/ocaml-cohttp-0.9.8.tar.gz",
             "file:///code/ocaml-cohttp-extra#ocaml-cohttp-extra-0.9.8.tar.gz",
             "ocaml-cohttp-init"])

    def test_source_paths(self):
        self.assertEqual(
            self.spec.source_paths(),
            ["./SOURCES/ocaml-cohttp-0.9.8.tar.gz",
             "./SOURCES/ocaml-cohttp-extra-0.9.8.tar.gz",
             "./SOURCES/ocaml-cohttp-init"])

    def test_buildrequires(self):
        self.assertEqual(
            self.spec.buildrequires(),
            set(["ocaml", "ocaml-findlib", "ocaml-re-devel",
                 "ocaml-uri-devel", "ocaml-cstruct-devel",
                 "ocaml-lwt-devel", "ocaml-ounit-devel",
                 "ocaml-ocamldoc", "ocaml-camlp4-devel",
                 "openssl", "openssl-devel"]))

    def test_source_package_path(self):
        self.assertEqual(
            self.spec.source_package_path(),
            "./SRPMS/ocaml-cohttp-0.9.8-1.el6.src.rpm")

    def test_binary_package_paths(self):
        machine = get_rpm_machine()

        self.assertEqual(
            sorted(self.spec.binary_package_paths()),
            [
                path.format(machine=machine) for path in
                sorted([
                    "./RPMS/{machine}/ocaml-cohttp-0.9.8-1.el6.{machine}.rpm",
                    "./RPMS/{machine}/" +
                    "ocaml-cohttp-devel-0.9.8-1.el6.{machine}.rpm"])
            ]
        )


class DebTests(unittest.TestCase):
    def setUp(self):
        # 'setUp' breaks Pylint's naming rules
        # pylint: disable=C0103
        def map_rpm_to_deb(name):
            mapping = {"ocaml-cohttp": ["libcohttp-ocaml"],
                       "ocaml-cohttp-devel": ["libcohttp-ocaml-dev"],
                       "ocaml": ["ocaml-nox", "ocaml-native-compilers"],
                       "ocaml-findlib": ["ocaml-findlib"],
                       "ocaml-re-devel": ["libre-ocaml-dev"],
                       "ocaml-uri-devel": ["liburi-ocaml-dev"],
                       "ocaml-cstruct-devel": ["libcstruct-ocaml-dev"],
                       "ocaml-lwt-devel": ["liblwt-ocaml-dev"],
                       "ocaml-ounit-devel": ["libounit-ocaml-dev"],
                       "ocaml-ocamldoc": ["ocaml-nox"],
                       "ocaml-camlp4-devel": ["camlp4", "camlp4-extra"],
                       "openssl": ["libssl1.0.0"],
                       "openssl-devel": ["libssl-dev"]}
            return mapping[name]

        self.spec = planex.spec.Spec("./tests/data/ocaml-cohttp.spec",
                                     target="deb",
                                     map_name=map_rpm_to_deb)

    def test_name(self):
        self.assertEqual(self.spec.name(), "ocaml-cohttp")

    def test_specpath(self):
        self.assertEqual(self.spec.specpath(), "./SPECS/ocaml-cohttp.spec")

    def test_version(self):
        self.assertEqual(self.spec.version(), "0.9.8")

    def test_provides(self):
        self.assertEqual(
            self.spec.provides(),
            set(["libcohttp-ocaml", "libcohttp-ocaml-dev"]))

    def test_source_urls(self):
        self.assertEqual(
            self.spec.source_urls(),
            ["https://github.com/mirage/ocaml-cohttp/archive/" +
             "ocaml-cohttp-0.9.8/ocaml-cohttp-0.9.8.tar.gz",
             "file:///code/ocaml-cohttp-extra#ocaml-cohttp-extra-0.9.8.tar.gz",
             "ocaml-cohttp-init"])

    def test_source_paths(self):
        self.assertEqual(
            self.spec.source_paths(),
            ["./SOURCES/ocaml-cohttp-0.9.8.tar.gz",
             "./SOURCES/ocaml-cohttp-extra-0.9.8.tar.gz",
             "./SOURCES/ocaml-cohttp-init"])

    def test_buildrequires(self):
        self.assertEqual(
            self.spec.buildrequires(),
            set(["ocaml-nox", "ocaml-native-compilers",
                 "ocaml-findlib", "libre-ocaml-dev",
                 "liburi-ocaml-dev", "libcstruct-ocaml-dev",
                 "liblwt-ocaml-dev", "libounit-ocaml-dev",
                 "camlp4", "camlp4-extra", "libssl1.0.0",
                 "libssl-dev"]))

    def test_source_package_path(self):
        self.assertEqual(
            self.spec.source_package_path(),
            "./SRPMS/libcohttp-ocaml_0.9.8-1.dsc")

    def test_binary_package_paths(self):
        machine = get_deb_machine()

        self.assertEqual(
            sorted(self.spec.binary_package_paths()),
            [path.format(machine=machine) for path
             in sorted(["./RPMS/libcohttp-ocaml_0.9.8-1_{machine}.deb",
                        "./RPMS/libcohttp-ocaml-dev_0.9.8-1_{machine}.deb"])])
