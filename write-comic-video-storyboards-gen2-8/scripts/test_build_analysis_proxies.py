from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from build_analysis_proxies import build_overview, image_paths, proxy_one

SCRIPT = Path(__file__).with_name("build_analysis_proxies.py")


class AnalysisProxyTests(unittest.TestCase):
    def test_overview_paginates_preserves_order_and_unicode_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "原图"
            source.mkdir()
            for number in reversed(range(1, 15)):
                Image.new("RGB", (80, 160), (number * 10, 20, 30)).save(
                    source / f"第16話_{number:02d}_001.png"
                )
            paths = image_paths(source)
            originals = {path: path.read_bytes() for path in paths}
            rows = [proxy_one(path, root / "proxy" / path.name) for path in paths]
            manifest = build_overview(rows, root / "overview")
            self.assertEqual(manifest["panel_count"], 14)
            self.assertEqual([len(s["panels"]) for s in manifest["sheets"]], [12, 2])
            entries = [entry for sheet in manifest["sheets"] for entry in sheet["panels"]]
            self.assertEqual([entry["index"] for entry in entries], list(range(1, 15)))
            self.assertEqual([entry["filename"] for entry in entries], [p.name for p in paths])
            for sheet in manifest["sheets"]:
                with Image.open(sheet["path"]) as image:
                    self.assertLessEqual(image.width, 1280)
                    self.assertLessEqual(image.height, 720)
                    # Check that thumbnails occupy their numbered cells in source order.
                    for i, entry in enumerate(sheet["panels"]):
                        x, y = (i % 4) * 320 + 160, (i // 4) * 208 + 80
                        self.assertAlmostEqual(image.getpixel((x, y))[0], entry["index"] * 10, delta=5)
            saved = json.loads(Path(manifest["index"]).read_text(encoding="utf-8"))
            self.assertEqual(saved["sheets"], manifest["sheets"])
            self.assertEqual({path: path.read_bytes() for path in paths}, originals)

    def test_cli_overview_reuses_proxies_without_marking_visual_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "panel.png"
            Image.new("RGB", (900, 1800), "white").save(source)
            command = [sys.executable, str(SCRIPT), str(source), "--output-dir", str(root / "proxy"), "--overview"]
            for expected_cached in (False, True):
                result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                manifest = json.loads(result.stdout)
                self.assertEqual(manifest["images"][0]["cached"], expected_cached)
                self.assertEqual(manifest["overview"]["panel_count"], 1)
                self.assertNotIn("source_audit", result.stdout)
                self.assertNotIn("viewed_while_writing", result.stdout)

    def test_output_cannot_overwrite_source_even_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "panel.jpg"
            Image.new("RGB", (1080, 1080), "white").save(source)
            original = source.read_bytes()
            with self.assertRaisesRegex(ValueError, "overwrite"):
                proxy_one(source, source, force=True)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--output-dir", str(root), "--force", "--overview"],
                capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not overwrite", result.stderr)
            self.assertEqual(source.read_bytes(), original)
            self.assertFalse((root / "overview").exists())

    def test_empty_overview_has_no_fake_sheet(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = build_overview([], Path(temp_dir))
            self.assertEqual(manifest["panel_count"], 0)
            self.assertEqual(manifest["sheets"], [])

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
