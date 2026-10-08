"""Exercise rejected gate inputs without modifying the intentional-bug app."""
import unittest
from validate_workshop import KNOWN_WARNING, VERSIONS, frozen_sources, test_gate, warning_gate


class ValidatorGateTests(unittest.TestCase):
    def test_frozen_sources_rejects_changed_or_missing_baseline(self):
        self.assertEqual(frozen_sources({})['status'], 'FAIL')
        drifted = {v: {'source_sha256': {'requirements.txt': '0' * 64}} for v in VERSIONS}
        result = frozen_sources(drifted)
        self.assertEqual(result['status'], 'FAIL')
        self.assertEqual(result['versions']['B0']['changed_files'], ['requirements.txt'])

    def test_same_count_different_b0_failure_is_rejected(self):
        manifest = [f'tests/unit/test_fare.py::test_{i}' for i in range(5)]
        changed = sorted(manifest[:-1] + ['tests/unit/test_fare.py::test_unknown'])
        self.assertFalse(test_gate({'passed': 39, 'skipped': 0, 'failed': 5},
                                   changed, [], 'B0', VERSIONS['B0'], manifest))
        self.assertTrue(test_gate({'passed': 39, 'skipped': 0, 'failed': 5},
                                  sorted(manifest), [], 'B0', VERSIONS['B0'], manifest))

    def test_xfail_is_rejected_for_controlled_skip_gate(self):
        self.assertFalse(test_gate({'passed': 1, 'skipped': 8, 'failed': 0}, [],
            [{'type': 'pytest.xfail'}] * 8, 'G0', VERSIONS['G0'], []))

    def test_unknown_warning_alongside_known_warning_is_rejected(self):
        known = ': '.join(KNOWN_WARNING)
        self.assertTrue(warning_gate(known)[1])
        self.assertFalse(warning_gate(known + '\nRuntimeWarning: new issue')[1])
        self.assertFalse(warning_gate('Custom_1Warning: unknown issue')[1])
        self.assertFalse(warning_gate('package.Custom_Warning: unknown issue')[1])
        self.assertFalse(warning_gate('Warning: unknown issue')[1])


if __name__ == '__main__':
    unittest.main()
