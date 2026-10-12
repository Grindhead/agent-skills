import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/validate_skills.py'

class ValidatorTests(unittest.TestCase):
    def run_validator(self, root, *args):
        return subprocess.run(['python3', str(SCRIPT), str(root), *args], capture_output=True, text=True)

    def test_reference_and_strict_modes_ignore_sample_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / 'demo'
            skill.mkdir()
            (skill / 'SKILL.md').write_text('---\nname: demo\ndescription: Example\n---\nUse /missing. Invoke `/demo`.\n```bash\n/tmp/fake\n```\nSample /usr/bin/file and **bold prose**.\n')
            default = self.run_validator(root)
            self.assertEqual(default.returncode, 0)
            result = json.loads(default.stdout)['results']['demo']
            self.assertEqual(result['issues'], [])
            self.assertEqual(len(result['warnings']), 1)
            self.assertIn('/missing', result['warnings'][0])
            self.assertEqual(self.run_validator(root, '--strict').returncode, 0)
            self.assertEqual(self.run_validator(root, '--strict-warnings').returncode, 1)
            (skill / 'SKILL.md').write_text('bad frontmatter')
            self.assertEqual(self.run_validator(root, '--strict').returncode, 1)

if __name__ == '__main__':
    unittest.main()
