from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).with_name("build_analysis_proxies.py")


class AnalysisProxyTests(unittest.TestCase):
    def test_proxy_fits_720p_without_replacing_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source" / "panel.jpg"
            output = root / "proxy"
            source.parent.mkdir()
            Image.new("RGB", (1080, 1080), "white").save(source)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source.parent), "--output-dir", str(output)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with Image.open(source) as original:
                self.assertEqual(original.size, (1080, 1080))
            with Image.open(output / "panel.jpg") as proxy:
                self.assertEqual(proxy.size, (720, 720))


if __name__ == "__main__":
    unittest.main()
