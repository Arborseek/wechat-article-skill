from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_workbuddy_package as workbuddy  # noqa: E402


class WorkBuddyPackageTests(unittest.TestCase):
    def test_package_has_expected_root_metadata_and_resources(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "wechat-article-skill-workbuddy.zip"
            workbuddy.build_package(ROOT, output)

            with ZipFile(output) as archive:
                names = set(archive.namelist())
                prefix = "skills/wechat-article-skill/"
                expected = {
                    prefix + "SKILL.md",
                    prefix + "requirements.txt",
                    prefix + "references/style-system.md",
                    prefix + "scripts/style_article_html.py",
                    prefix + "schemas/article-package.schema.json",
                }
                self.assertFalse(expected - names)
                manifest = archive.read(prefix + "SKILL.md").decode("utf-8")

            for field in (
                "description_zh:",
                "description_en:",
                "version:",
                "author:",
                "user-invocable: true",
            ):
                self.assertIn(field, manifest)
            self.assertEqual(manifest.count("# WeChat Article Skill"), 1)


if __name__ == "__main__":
    unittest.main()
