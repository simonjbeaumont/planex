import unittest
import os

from planex import clone

MANDATORY_ARGS = ['config_dir']


class TestParseArgsOrExit(unittest.TestCase):
    def test_quiet_defaults_to_false(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS)

        self.assertEquals(False, args.quiet)

    def test_quiet_set_to_true(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS + ['--quiet'])

        self.assertEquals(True, args.quiet)

    def test_dry_run_defaults_to_false(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS)

        self.assertEquals(False, args.dry_run)

    def test_dry_run_set_to_true(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS + ['--dry-run'])

        self.assertEquals(True, args.dry_run)

    def test_print_only_defaults_to_false(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS)

        self.assertEquals(False, args.print_only)

    def test_print_only_specified(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS + ['--print-only'])

        self.assertEquals(True, args.print_only)

    def test_correct_call(self):
        args = clone.parse_args_or_exit(['config_dir'])

        self.assertEquals('config_dir', args.config_dir)

    def test_incorrect_call(self):
        self.assertRaises(SystemExit, clone.parse_args_or_exit, [])

    def test_repos_path_set(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS +
                                        ['--repos_path', '/foo'])
        self.assertEquals('/foo', args.repos_path)

    def test_repos_path_unset(self):
        args = clone.parse_args_or_exit(MANDATORY_ARGS)
        self.assertEquals('repos', args.repos_path)
