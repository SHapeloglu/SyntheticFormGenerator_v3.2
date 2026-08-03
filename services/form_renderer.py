from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


class RenderError(RuntimeError):
    """Form görüntüsü üretimi sırasında oluşan hata."""


def load_coordinates(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"pages": {}}

    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return {"pages": {}}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RenderError(
            f"Koordinat dosyası geçersiz JSON: satır {exc.lineno}, sütun {exc.colno}"
        ) from exc

    if not isinstance(data, dict):
        raise RenderError("Koordinat dosyasının kök değeri nesne olmalıdır.")

    data.setdefault("pages", {})
    return data


def save_coordinates(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _get_font(size: int = 28) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/segoepr.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)

    return ImageFont.load_default()


def render_page(
    template_path: Path,
    output_path: Path,
    record: dict[str, Any],
    fields: dict[str, Any],
) -> Path:
    if not template_path.exists():
        raise RenderError(f"Form şablonu bulunamadı: {template_path}")

    image = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    for field_name, config in fields.items():
        value = record.get(field_name, "")
        if value in (None, ""):
            continue

        x = int(config.get("x", 0))
        y = int(config.get("y", 0))
        font_size = int(config.get("font_size", 28))
        font = _get_font(font_size)

        draw.text((x, y), str(value), fill=(20, 45, 110), font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, quality=95)
    return output_path
