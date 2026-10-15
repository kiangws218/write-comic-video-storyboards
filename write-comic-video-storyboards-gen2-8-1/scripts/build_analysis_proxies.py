from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from PIL import Image, ImageOps


SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}
BOUND = (1280, 720)


def cache_dir(source: Path) -> Path:
    key = hashlib.sha256(str(source.resolve()).encode("utf-8")).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / "comic-storyboard-720p" / key


def proxy_one(source: Path, destination: Path, force: bool = False) -> dict[str, object]:
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build non-destructive 1280x720 analysis proxies for comic panels."
    )
    parser.add_argument("source", type=Path, help="panel image or panel directory")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--force", action="store_true")
    arguments = parser.parse_args()

    source = arguments.source.resolve()
    output = (arguments.output_dir or cache_dir(source)).resolve()
    rows = [proxy_one(path, output / path.name, arguments.force) for path in image_paths(source)]
    print(json.dumps({"output_dir": str(output), "images": rows}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
