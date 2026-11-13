from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}
BOUND = (1280, 720)
THUMB_BOUND = (320, 180)
OVERVIEW_COLUMNS = 4
OVERVIEW_PAGE_SIZE = 12
OVERVIEW_CELL_HEIGHT = 208


def cache_dir(source: Path) -> Path:
    key = hashlib.sha256(str(source.resolve()).encode("utf-8")).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / "comic-storyboard-720p" / key


def proxy_one(source: Path, destination: Path, force: bool = False) -> dict[str, object]:
    if source.resolve() == destination.resolve():
        raise ValueError("analysis output must not overwrite a source image")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if (
        not force
        and destination.exists()
        and destination.stat().st_mtime_ns >= source.stat().st_mtime_ns
    ):
        with Image.open(destination) as cached:
            return {
                "source": str(source.resolve()),
                "proxy": str(destination.resolve()),
                "size": list(cached.size),
                "cached": True,
            }

    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        original_size = image.size
        image.thumbnail(BOUND, Image.Resampling.LANCZOS)
        if destination.suffix.casefold() in {".jpg", ".jpeg"}:
            image = image.convert("RGB")
            image.save(destination, quality=90, optimize=True)
        elif destination.suffix.casefold() == ".png":
            image.save(destination, optimize=True)
        else:
            image.save(destination, quality=90, method=6)
        return {
            "source": str(source.resolve()),
            "proxy": str(destination.resolve()),
            "original_size": list(original_size),
            "size": list(image.size),
            "cached": False,
        }


def image_paths(source: Path) -> list[Path]:
    if source.is_file():
        if source.suffix.casefold() not in SUPPORTED:
            raise ValueError(f"unsupported image type: {source}")
        return [source]
    if not source.is_dir():
        raise FileNotFoundError(source)
    return sorted(
        path for path in source.iterdir() if path.is_file() and path.suffix.casefold() in SUPPORTED
    )


def build_overview(rows: list[dict[str, object]], output: Path) -> dict[str, object]:
    """Make a paginated orientation index, never a visual-inspection attestation."""
    output.mkdir(parents=True, exist_ok=True)
    sheets = []
    for offset in range(0, len(rows), OVERVIEW_PAGE_SIZE):
        page = rows[offset : offset + OVERVIEW_PAGE_SIZE]
        row_count = (len(page) + OVERVIEW_COLUMNS - 1) // OVERVIEW_COLUMNS
        sheet = Image.new(
            "RGB", (OVERVIEW_COLUMNS * THUMB_BOUND[0], row_count * OVERVIEW_CELL_HEIGHT),
            "#e4e4e4",
        )
        draw = ImageDraw.Draw(sheet)
        entries = []
        for cell_index, row in enumerate(page):
            proxy = Path(str(row["proxy"]))
            x = (cell_index % OVERVIEW_COLUMNS) * THUMB_BOUND[0]
            y = (cell_index // OVERVIEW_COLUMNS) * OVERVIEW_CELL_HEIGHT
            with Image.open(proxy) as opened:
                thumb = ImageOps.exif_transpose(opened).convert("RGB")
                thumb.thumbnail(THUMB_BOUND, Image.Resampling.LANCZOS)
                sheet.paste(thumb, (x + (THUMB_BOUND[0] - thumb.width) // 2, y))
            number = offset + cell_index + 1
            # ASCII numbers remain readable without a platform-specific CJK font.
            # The durable index maps each number to its exact Unicode filename.
            draw.text((x + 8, y + THUMB_BOUND[1] + 6), f"{number:06d}", fill="black")
            entries.append({
                "index": number, "filename": Path(str(row["source"])).name,
                "proxy": str(proxy),
            })
        destination = output / f"overview-{offset // OVERVIEW_PAGE_SIZE + 1:04d}.jpg"
        sheet.save(destination, quality=85, optimize=True)
        sheets.append({"path": str(destination.resolve()), "panels": entries})
    manifest = {"sheets": sheets, "panel_count": len(rows)}
    index_path = output / "index.json"
    index_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"index": str(index_path.resolve()), **manifest}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build non-destructive 1280x720 analysis proxies for comic panels."
    )
    parser.add_argument("source", type=Path, help="panel image or panel directory")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--overview", action="store_true",
        help="also build numbered thumbnail sheets (up to 12 panels each) and a filename index",
    )
    arguments = parser.parse_args()

    source = arguments.source.resolve()
    output = (arguments.output_dir or cache_dir(source)).resolve()
    sources = image_paths(source)
    if any(path.resolve() == (output / path.name).resolve() for path in sources):
        parser.error("output directory must not overwrite source images")
    rows = [proxy_one(path, output / path.name, arguments.force) for path in sources]
    result = {"output_dir": str(output), "images": rows}
    if arguments.overview:
        result["overview"] = build_overview(rows, output / "overview")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
