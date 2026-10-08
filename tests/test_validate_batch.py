import json

import pytest

from services.batch_storage import save_batch, validate_batch

BATCH_ID = "BATCH-20261008_000000_000000"


def kayitlar(*form_ids):
    return [{"Form ID": form_id} for form_id in form_ids]


def metadata(records):
    ids = [r["Form ID"] for r in records]
    return {"count": len(records), "first_form_id": ids[0], "last_form_id": ids[-1]}


def batch_yaz(tmp_path, records, meta=None, xlsx=True):
    save_batch(tmp_path, BATCH_ID, records, meta if meta is not None else metadata(records))
    if xlsx:
        (tmp_path / BATCH_ID / "ground_truth.xlsx").write_bytes(b"")


def test_saglam_batch(tmp_path):
    batch_yaz(tmp_path, kayitlar("FORM-00001", "FORM-00002", "FORM-00003"))
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert sonuc["ok"], sonuc["errors"]
    assert sonuc["record_count"] == 3
    assert (sonuc["first_form_id"], sonuc["last_form_id"]) == ("FORM-00001", "FORM-00003")


def test_json_yok(tmp_path):
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert not sonuc["ok"]
    assert "ground_truth.json bulunamadı." in sonuc["errors"]


def test_xlsx_yok(tmp_path):
    batch_yaz(tmp_path, kayitlar("FORM-00001"), xlsx=False)
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert "ground_truth.xlsx bulunamadı." in sonuc["errors"]


def test_bozuk_json(tmp_path):
    hedef = tmp_path / BATCH_ID
    hedef.mkdir()
    (hedef / "ground_truth.json").write_text("{bozuk", encoding="utf-8")
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert not sonuc["ok"]
    assert any(e.startswith("ground_truth.json okunamadı") for e in sonuc["errors"])


def test_records_liste_degil(tmp_path):
    hedef = tmp_path / BATCH_ID
    hedef.mkdir()
    (hedef / "ground_truth.json").write_text(json.dumps({"metadata": {"count": 0}, "records": {}}), encoding="utf-8")
    (hedef / "ground_truth.xlsx").write_bytes(b"")
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert "JSON içindeki records alanı liste değil." in sonuc["errors"]


def test_tekrarlanan_form_id(tmp_path):
    batch_yaz(tmp_path, kayitlar("FORM-00001", "FORM-00002", "FORM-00001"))
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert "Tekrarlanan Form ID: FORM-00001" in sonuc["errors"]


def test_eksik_form_id(tmp_path):
    records = kayitlar("FORM-00001", "", "FORM-00003")
    batch_yaz(tmp_path, records, {"count": 3, "first_form_id": "FORM-00001", "last_form_id": "FORM-00003"})
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert "1 kayıtta Form ID eksik." in sonuc["errors"]


def test_metadata_sayi_uyusmazligi(tmp_path):
    records = kayitlar("FORM-00001", "FORM-00002")
    batch_yaz(tmp_path, records, {**metadata(records), "count": 5})
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert "Metadata count=5, gerçek kayıt=2." in sonuc["errors"]


def test_ilk_son_form_id_uyusmazligi(tmp_path):
    records = kayitlar("FORM-00001", "FORM-00002")
    batch_yaz(tmp_path, records, {"count": 2, "first_form_id": "FORM-00009", "last_form_id": "FORM-00008"})
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert "İlk Form ID metadata ile eşleşmiyor." in sonuc["errors"]
    assert "Son Form ID metadata ile eşleşmiyor." in sonuc["errors"]


def test_hic_form_id_yoksa_uyari(tmp_path):
    hedef = tmp_path / BATCH_ID
    hedef.mkdir()
    (hedef / "ground_truth.json").write_text(json.dumps({"metadata": {"count": 0}, "records": []}), encoding="utf-8")
    (hedef / "ground_truth.xlsx").write_bytes(b"")
    sonuc = validate_batch(tmp_path, BATCH_ID)
    assert sonuc["ok"]
    assert sonuc["warnings"] == ["Batch içinde Form ID içeren kayıt yok."]


@pytest.mark.parametrize("kotu_id", ["../BATCH-x", "BATCH-a/b", "FORM-1", "BATCH-..\\x"])
def test_guvensiz_batch_id_reddedilir(tmp_path, kotu_id):
    with pytest.raises(ValueError):
        validate_batch(tmp_path, kotu_id)
