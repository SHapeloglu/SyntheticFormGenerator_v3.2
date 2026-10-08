from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

from services.batch_storage import (
    archive_batch, list_archived_batches, list_batches, load_batch, restore_batch,
    save_batch, search_form, validate_batch,
)
from services.data_generator import FORM_SCHEMA, assign_test_split, generate_records, ocr_ground_truth
from services.excel_exporter import create_excel
from services.form_renderer import RenderError, load_coordinates, render_page, save_coordinates
from services.sequence_manager import reserve_sequence

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
BATCH_DIR = OUTPUT_DIR / "batches"
ARCHIVE_DIR = OUTPUT_DIR / "archive"
STATIC_DIR = BASE_DIR / "static"
FORM_DIR = STATIC_DIR / "forms"
COORDINATES_PATH = BASE_DIR / "config" / "coordinates.json"
SEQUENCE_PATH = BASE_DIR / "config" / "sequence.json"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

app = Flask(__name__)
# Yerel araç için sabit yedek; ağa açılırsa SFG_SECRET_KEY ortam değişkeniyle verilmeli.
app.secret_key = os.environ.get("SFG_SECRET_KEY", "synthetic-form-generator-local-secret")
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    FORM_DIR.mkdir(parents=True, exist_ok=True)


def card_groups(record: dict) -> list[tuple[str, list[tuple[str, object]]]]:
    """Kart bölümleri form şemasından gelir (matbu formdaki sırayla); boş alanlar kartta görünmez."""
    sections: dict[str, list[tuple[str, object]]] = {}
    for _key, label, page, section in FORM_SCHEMA:
        value = record.get(label, "")
        if value not in (None, ""):
            sections.setdefault(f"Sayfa {page} · {section}", []).append((label, value))
    return list(sections.items())


def simplified_fields(record: dict) -> list[tuple[str, object]]:
    keys = [
        "Adı Soyadı", "T.C. Kimlik No", "Doğum Yeri ve Tarihi", "Cinsiyeti", "Eğitim Durumu",
        "Medeni Durumu", "Tel (Cep)", "Ev Adresi", "Mesleği", "Yaptığı İş", "Çalıştığı Bölüm",
        "Kan Grubu", "Bilinen Alerji Öyküsü", "Konjenital / Kronik Hastalık", "TA (tansiyon)",
        "Nabız", "Boy", "Kilo", "Onay Tarihi",
    ]
    return [(key, record.get(key, "")) for key in keys if record.get(key, "") not in (None, "")]


def write_ocr_ground_truth(batch_path: Path, records: list[dict]) -> None:
    """faz1-trocr-main data/cikti/ground_truth/ biçimi: <OCR ID>.json, düz {alan: değer}.
    Taramalar <OCR ID>1.jpeg / <OCR ID>2.jpeg olarak adlandırılır."""
    target = batch_path / "ocr_ground_truth"
    target.mkdir(exist_ok=True)
    for record in records:
        (target / f"{record['OCR ID']}.json").write_text(
            json.dumps(ocr_ground_truth(record), ensure_ascii=False, indent=2), encoding="utf-8")


@app.get("/")
def index():
    ensure_dirs()
    return render_template("index.html", batches=list_batches(BATCH_DIR)[:10])


@app.post("/batch/create")
def create_batch():
    try:
        count = int(request.form.get("count", "50"))
        fill_rate = int(request.form.get("fill_rate", "90"))
        doctor_profile = request.form.get("doctor_profile", "random")
        repeat_rate = int(request.form.get("repeat_rate", "10"))
        test_count = int(request.form.get("test_count", "10" if count >= 20 else "0"))
        if not 0 <= test_count < count:
            raise ValueError("Test seti form sayısı 0 ile toplamın bir eksiği arasında olmalıdır.")
        start_number = reserve_sequence(SEQUENCE_PATH, count)
        # Kişi numarası (ve sentetik TC) Form ID aralığından gelir → batch'ler arasında çakışmaz.
        records = generate_records(
            count=count,
            fill_rate=fill_rate,
            doctor_profile=doctor_profile,
            start_index=start_number,
            repeat_rate=repeat_rate,
        )
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        batch_id = f"BATCH-{timestamp}"
        for offset, record in enumerate(records):
            form_number = start_number + offset
            record["Form ID"] = f"FORM-{form_number:05d}"
            record["OCR ID"] = f"sfg{form_number:05d}"
        test_ids = assign_test_split(records, test_count)
        metadata = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "count": count,
            "fill_rate": fill_rate,
            "doctor_profile": doctor_profile,
            "repeat_rate": repeat_rate,
            "test_form_ids": test_ids,
            "first_form_id": f"FORM-{start_number:05d}",
            "last_form_id": f"FORM-{start_number + count - 1:05d}",
        }
        save_batch(BATCH_DIR, batch_id, records, metadata)
        batch_path = BATCH_DIR / batch_id
        create_excel(records, batch_path / "ground_truth.xlsx")
        write_ocr_ground_truth(batch_path, records)
        validation = validate_batch(BATCH_DIR, batch_id)
        if not validation["ok"]:
            raise RuntimeError("Batch doğrulaması başarısız: " + "; ".join(validation["errors"]))
        return render_template(
            "batch.html", batch_id=batch_id, records=records,
            metadata=metadata, validation=validation, mode="summary", card_groups=card_groups,
            simplified_fields=simplified_fields,
        )
    except ValueError as exc:
        return render_template("index.html", error=str(exc), batches=list_batches(BATCH_DIR)[:10]), 400
    except Exception as exc:
        app.logger.exception("Toplu veri üretme hatası")
        return render_template("index.html", error=f"Beklenmeyen hata: {exc}", batches=list_batches(BATCH_DIR)[:10]), 500


@app.get("/batch/<batch_id>")
def batch_summary(batch_id: str):
    try:
        payload = load_batch(BATCH_DIR, batch_id)
    except FileNotFoundError:
        abort(404)
    return render_template(
        "batch.html", batch_id=batch_id, records=payload["records"], metadata=payload["metadata"],
        validation=validate_batch(BATCH_DIR, batch_id), mode="summary",
        card_groups=card_groups, simplified_fields=simplified_fields,
    )


@app.get("/batch/<batch_id>/cards")
def batch_cards(batch_id: str):
    try:
        payload = load_batch(BATCH_DIR, batch_id)
    except FileNotFoundError:
        abort(404)
    mode = request.args.get("mode", "detailed")
    if mode not in {"detailed", "simple"}:
        mode = "detailed"
    return render_template(
        "cards.html", batch_id=batch_id, records=payload["records"], mode=mode,
        card_groups=card_groups, simplified_fields=simplified_fields,
        pdf=request.args.get("pdf") == "1",
    )


@app.get("/batch/<batch_id>/download/<kind>")
def batch_download(batch_id: str, kind: str):
    batch_path = BATCH_DIR / batch_id
    if kind == "xlsx":
        path = batch_path / "ground_truth.xlsx"
        mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif kind == "json":
        path = batch_path / "ground_truth.json"
        mimetype = "application/json"
    elif kind == "zip":
        path = batch_path / f"{batch_id}.zip"
        with ZipFile(path, "w", ZIP_DEFLATED) as archive:
            for source in sorted(batch_path.rglob("*")):
                if source.is_file() and source != path:
                    archive.write(source, arcname=source.relative_to(batch_path))
        mimetype = "application/zip"
    else:
        abort(404)
    if not path.exists():
        abort(404)
    return send_file(path, as_attachment=True, download_name=path.name, mimetype=mimetype)


@app.get("/batches")
def batches_page():
    ensure_dirs()
    return render_template(
        "batches.html",
        batches=list_batches(BATCH_DIR, include_validation=True),
        archived_batches=list_archived_batches(ARCHIVE_DIR),
    )


@app.get("/search")
def form_search():
    query = request.args.get("form_id", "").strip().upper()
    results = search_form(BATCH_DIR, query) if query else []
    return render_template("search.html", query=query, results=results)


@app.post("/batch/<batch_id>/archive")
def batch_archive(batch_id: str):
    confirmation = request.form.get("confirmation", "").strip()
    if confirmation != batch_id:
        flash("Arşivleme için batch adını doğru yazmalısınız.", "error")
        return redirect(url_for("batch_summary", batch_id=batch_id))
    try:
        archive_batch(BATCH_DIR, ARCHIVE_DIR, batch_id)
        flash(f"{batch_id} arşivlendi.", "success")
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        flash(str(exc), "error")
    return redirect(url_for("batches_page"))


@app.post("/batch/<batch_id>/restore")
def batch_restore(batch_id: str):
    try:
        restore_batch(BATCH_DIR, ARCHIVE_DIR, batch_id)
        flash(f"{batch_id} arşivden geri alındı.", "success")
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        flash(str(exc), "error")
    return redirect(url_for("batches_page"))


@app.get("/batch/<batch_id>/validate")
def batch_validate(batch_id: str):
    try:
        return jsonify(validate_batch(BATCH_DIR, batch_id))
    except ValueError as exc:
        return jsonify({"ok": False, "errors": [str(exc)]}), 400


# Eski tek-adımlı Excel uç noktası geriye uyumluluk için korunur.
@app.post("/generate")
def generate():
    return create_batch()


@app.get("/batch/<batch_id>/preview/<form_id>/<page_key>")
def form_preview(batch_id: str, form_id: str, page_key: str):
    try:
        payload = load_batch(BATCH_DIR, batch_id)
    except (FileNotFoundError, ValueError):
        abort(404)
    record = next((r for r in payload["records"] if str(r.get("Form ID", "")).upper() == form_id.upper()), None)
    page = load_coordinates(COORDINATES_PATH).get("pages", {}).get(page_key)
    if record is None or not page or not page.get("image"):
        abort(404)
    output_path = BATCH_DIR / batch_id / "preview" / f"{secure_filename(form_id)}_{secure_filename(page_key)}.jpg"
    try:
        render_page(FORM_DIR / page["image"], output_path, record, page.get("fields", {}))
    except RenderError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 404
    return send_file(output_path, mimetype="image/jpeg")


@app.get("/coordinates")
def coordinates_editor():
    coordinates = load_coordinates(COORDINATES_PATH)
    page_files = sorted([file.name for file in FORM_DIR.glob("*") if file.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS])
    sample_record = generate_records(count=1, fill_rate=100)[0]
    return render_template("coordinates.html", page_files=page_files, field_names=list(sample_record.keys()), coordinates=coordinates)


@app.post("/coordinates/upload")
def upload_form_page():
    uploaded_file = request.files.get("form_image")
    page_key = request.form.get("page_key", "page1").strip() or "page1"
    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"ok": False, "error": "Bir form görseli seçilmelidir."}), 400
    extension = Path(uploaded_file.filename).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({"ok": False, "error": "Yalnızca JPG, JPEG, PNG veya WEBP yüklenebilir."}), 400
    filename = secure_filename(f"{page_key}{extension}")
    uploaded_file.save(FORM_DIR / filename)
    coordinates = load_coordinates(COORDINATES_PATH)
    page = coordinates.setdefault("pages", {}).setdefault(page_key, {})
    page["image"] = filename
    page.setdefault("fields", {})
    save_coordinates(COORDINATES_PATH, coordinates)
    return jsonify({"ok": True, "filename": filename, "image_url": f"/static/forms/{filename}", "page_key": page_key})


@app.post("/coordinates/save")
def save_field_coordinate():
    payload = request.get_json(silent=True) or {}
    page_key = str(payload.get("page_key", "")).strip()
    field_name = str(payload.get("field_name", "")).strip()
    if not page_key or not field_name:
        return jsonify({"ok": False, "error": "Sayfa ve alan adı zorunludur."}), 400
    try:
        field_config = {key: int(payload.get(key, 28 if key == "font_size" else 0)) for key in ("x", "y", "width", "height", "font_size")}
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "Koordinat değerleri geçersiz."}), 400
    coordinates = load_coordinates(COORDINATES_PATH)
    coordinates.setdefault("pages", {}).setdefault(page_key, {}).setdefault("fields", {})[field_name] = field_config
    save_coordinates(COORDINATES_PATH, coordinates)
    return jsonify({"ok": True, "field": field_name, "config": field_config})


@app.post("/coordinates/delete")
def delete_field_coordinate():
    payload = request.get_json(silent=True) or {}
    page_key = str(payload.get("page_key", "")).strip()
    field_name = str(payload.get("field_name", "")).strip()
    coordinates = load_coordinates(COORDINATES_PATH)
    fields = coordinates.get("pages", {}).get(page_key, {}).get("fields", {})
    fields.pop(field_name, None)
    save_coordinates(COORDINATES_PATH, coordinates)
    return jsonify({"ok": True})


if __name__ == "__main__":
    ensure_dirs()
    app.run(host="127.0.0.1", port=5000, debug=True)
