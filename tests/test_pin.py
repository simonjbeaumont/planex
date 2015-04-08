# Run these tests with 'nosetests':
#   install the 'python-nose' package (Fedora/CentOS or Ubuntu)
#   run 'nosetests' in the root of the repository

import unittest
import tempfile
import os
import shutil
from planex.pin import tag as git_tag
from planex.util import run


class GitTests(unittest.TestCase):
    # unittest.TestCase has more methods than Pylint permits
    # pylint: disable=R0904

    def setUp(self):
        self.repo_path = tempfile.mkdtemp(prefix='planex-pin-test')
        self.dotgitdir = os.path.join(self.repo_path, ".git")
        self.dummy_file = os.path.join(self.repo_path, "dummy")
        with open(self.dummy_file, 'w+') as dummy_file:
            dummy_file.write("Hello, world!")
        run(["git", "init", self.repo_path])
        run(["git", "--git-dir=%s" % self.dotgitdir,
             "config", "user.email", "you@example.com"])
        run(["git", "--git-dir=%s" % self.dotgitdir,
             "config", "user.name", "Your Name"])
        run(["git", "--git-dir=%s" % self.dotgitdir,
             "--work-tree=%s" % self.repo_path,
             "add", self.dummy_file])
        run(["git", "--git-dir=%s" % self.dotgitdir,
             "commit", "-m", "Initial commit"])

    def tearDown(self):
        shutil.rmtree(self.repo_path, True)

    def test_tag(self):
        old_tags = run(["git", "--git-dir=%s" % self.dotgitdir,
                        "tag"])['stdout'].split()
        git_tag(self.repo_path, "my-tag")
        current_tags = run(["git", "--git-dir=%s" % self.dotgitdir,
                            "tag"])['stdout'].split()
        new_tags = [t for t in current_tags if t not in old_tags]
        self.assertEqual(["my-tag"], new_tags)
