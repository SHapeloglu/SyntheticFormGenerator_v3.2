from __future__ import annotations

import json
import shutil
from datetime import date, datetime
from pathlib import Path
from typing import Any


def _json_default(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)


def _safe_batch_id(batch_id: str) -> str:
    batch_id = str(batch_id).strip()
    if not batch_id.startswith("BATCH-") or any(part in batch_id for part in ("/", "\\", "..")):
        raise ValueError("Geçersiz batch kimliği.")
    return batch_id


def save_batch(batch_dir: Path, batch_id: str, records: list[dict[str, Any]], metadata: dict[str, Any]) -> Path:
    batch_id = _safe_batch_id(batch_id)
    target_dir = batch_dir / batch_id
    target_dir.mkdir(parents=True, exist_ok=False)
    payload = {"metadata": metadata, "records": records}
    path = target_dir / "ground_truth.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8")
    return path


def load_batch(batch_dir: Path, batch_id: str) -> dict[str, Any]:
    batch_id = _safe_batch_id(batch_id)
    path = batch_dir / batch_id / "ground_truth.json"
    if not path.exists():
        raise FileNotFoundError("Toplu üretim kaydı bulunamadı.")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_batch(batch_dir: Path, batch_id: str) -> dict[str, Any]:
    """Batch dosyalarını ve metadata/record tutarlılığını denetler."""
    batch_id = _safe_batch_id(batch_id)
    target = batch_dir / batch_id
    errors: list[str] = []
    warnings: list[str] = []

    json_path = target / "ground_truth.json"
    xlsx_path = target / "ground_truth.xlsx"
    if not json_path.exists():
        errors.append("ground_truth.json bulunamadı.")
        return {"ok": False, "errors": errors, "warnings": warnings, "record_count": 0}
    if not xlsx_path.exists():
        errors.append("ground_truth.xlsx bulunamadı.")

    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"ground_truth.json okunamadı: {exc}")
        return {"ok": False, "errors": errors, "warnings": warnings, "record_count": 0}

    metadata = payload.get("metadata") or {}
    records = payload.get("records")
    if not isinstance(records, list):
        errors.append("JSON içindeki records alanı liste değil.")
        records = []

    form_ids = [str(r.get("Form ID", "")).strip() for r in records if isinstance(r, dict)]
    empty_ids = sum(1 for form_id in form_ids if not form_id)
    if empty_ids:
        errors.append(f"{empty_ids} kayıtta Form ID eksik.")

    nonempty_ids = [form_id for form_id in form_ids if form_id]
    duplicate_ids = sorted({form_id for form_id in nonempty_ids if nonempty_ids.count(form_id) > 1})
    if duplicate_ids:
        errors.append("Tekrarlanan Form ID: " + ", ".join(duplicate_ids[:10]))

    expected_count = metadata.get("count")
    if expected_count != len(records):
        errors.append(f"Metadata count={expected_count}, gerçek kayıt={len(records)}.")

    if nonempty_ids:
        if metadata.get("first_form_id") != nonempty_ids[0]:
            errors.append("İlk Form ID metadata ile eşleşmiyor.")
        if metadata.get("last_form_id") != nonempty_ids[-1]:
            errors.append("Son Form ID metadata ile eşleşmiyor.")
    else:
        warnings.append("Batch içinde Form ID içeren kayıt yok.")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "record_count": len(records),
        "first_form_id": nonempty_ids[0] if nonempty_ids else None,
        "last_form_id": nonempty_ids[-1] if nonempty_ids else None,
    }


def list_batches(batch_dir: Path, include_validation: bool = False) -> list[dict[str, Any]]:
    batches: list[dict[str, Any]] = []
    if not batch_dir.exists():
        return batches
    for path in sorted(batch_dir.glob("*/ground_truth.json"), reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            metadata = dict(payload.get("metadata", {}))
            metadata["batch_id"] = path.parent.name
            metadata["archived"] = False
            if include_validation:
                metadata["validation"] = validate_batch(batch_dir, path.parent.name)
            batches.append(metadata)
        except (OSError, json.JSONDecodeError, ValueError):
            continue
    return batches


def search_form(batch_dir: Path, form_id: str) -> list[dict[str, Any]]:
    query = str(form_id).strip().upper()
    if not query:
        return []
    results: list[dict[str, Any]] = []
    for batch in list_batches(batch_dir):
        try:
            payload = load_batch(batch_dir, batch["batch_id"])
        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            continue
        for record in payload.get("records", []):
            current = str(record.get("Form ID", "")).strip().upper()
            if current == query:
                results.append({"batch": batch, "record": record})
    return results


def archive_batch(batch_dir: Path, archive_dir: Path, batch_id: str) -> Path:
    batch_id = _safe_batch_id(batch_id)
    source = batch_dir / batch_id
    if not source.exists():
        raise FileNotFoundError("Batch bulunamadı.")
    archive_dir.mkdir(parents=True, exist_ok=True)
    target = archive_dir / batch_id
    if target.exists():
        raise FileExistsError("Bu batch zaten arşivde bulunuyor.")
    shutil.move(str(source), str(target))
    return target


def restore_batch(batch_dir: Path, archive_dir: Path, batch_id: str) -> Path:
    batch_id = _safe_batch_id(batch_id)
    source = archive_dir / batch_id
    if not source.exists():
        raise FileNotFoundError("Arşiv kaydı bulunamadı.")
    batch_dir.mkdir(parents=True, exist_ok=True)
    target = batch_dir / batch_id
    if target.exists():
        raise FileExistsError("Aynı kimlikte aktif batch zaten var.")
    shutil.move(str(source), str(target))
    return target


def list_archived_batches(archive_dir: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not archive_dir.exists():
        return items
    for path in sorted(archive_dir.glob("*/ground_truth.json"), reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            metadata = dict(payload.get("metadata", {}))
            metadata["batch_id"] = path.parent.name
            metadata["archived"] = True
            items.append(metadata)
        except (OSError, json.JSONDecodeError):
            continue
    return items
