import json
import random
import re
from pathlib import Path

import app as uygulama
from services.data_generator import FORM_SCHEMA, assign_test_split, generate_records, ocr_ground_truth

SABLON = Path("/root/faz1-trocr-main/sablon_koordinatlari.json")


def test_sema_faz1_sablonuyla_ayni():
    anahtarlar = [key for key, *_ in FORM_SCHEMA]
    assert len(anahtarlar) == len(set(anahtarlar)) == 92
    if SABLON.exists():
        sablon = json.loads(SABLON.read_text(encoding="utf-8"))
        assert set(anahtarlar) == set(sablon["sayfa1"]) | set(sablon["sayfa2"])


def test_tutarlilik_ve_bicimler():
    for tohum in range(60):
        random.seed(tohum)
        for kayit in generate_records(30, fill_rate=random.choice([0, 85, 100]), repeat_rate=20):
            dogum = kayit["Doğum Yeri ve Tarihi"]
            assert re.search(r" \d{2}[/.]\d{2}[/.]\d{4}$", dogum)
            assert re.fullmatch(r"\d{2}/\d{2}/\d{4}", kayit["Onay Tarihi"])
            yas = int(kayit["Onay Tarihi"][-4:]) - int(dogum[-4:])
            assert 17 <= yas <= 66
            assert re.fullmatch(r"05\d{9}", kayit["Tel (Cep)"])
            assert re.fullmatch(r"\d{2,3}/\d{2,3}", kayit["TA (tansiyon)"])
            assert re.fullmatch(r"(A|B|AB|0) [+-]", kayit["Kan Grubu"])
            for anahtar, etiket, *_ in FORM_SCHEMA:
                if anahtar.endswith("_hayir"):
                    soru = etiket.split(" → ")[0]
                    # Hayır daireliyse açıklama kutusu boş olmalı
                    assert not (kayit[etiket] == "Hayır" and kayit[soru])


def test_tekrar_muayene_ayni_kimlik_daha_gec_tarih():
    random.seed(3)
    kayitlar = generate_records(40, repeat_rate=25)
    kisiler: dict[str, list[dict]] = {}
    for kayit in kayitlar:
        kisiler.setdefault(kayit["Kişi No"], []).append(kayit)
    tekrarlar = [v for v in kisiler.values() if len(v) > 1]
    assert tekrarlar
    for formlar in tekrarlar:
        assert len({f["T.C. Kimlik No"] for f in formlar}) == 1
        assert len({f["Doğum Yeri ve Tarihi"] for f in formlar}) == 1
        assert {f["Muayene Türü"] for f in formlar} - {"İşe giriş"}


def test_test_seti_kisiyi_bolmez():
    random.seed(5)
    kayitlar = generate_records(50, repeat_rate=20)
    for i, kayit in enumerate(kayitlar):
        kayit["Form ID"] = f"FORM-{i:05d}"
    ids = assign_test_split(kayitlar, 10)
    assert len(ids) == 10
    for kisi in {k["Kişi No"] for k in kayitlar}:
        assert len({k["Kullanım"] for k in kayitlar if k["Kişi No"] == kisi}) == 1


def test_ocr_ground_truth_bos_kutu():
    random.seed(7)
    gt = ocr_ground_truth(generate_records(1, fill_rate=0)[0])
    assert gt["ta_diastolik"] == "boş"
    assert "" not in gt.values()


def test_batch_ocr_dosyalari_ve_kartlar(tmp_path, monkeypatch):
    monkeypatch.setattr(uygulama, "BATCH_DIR", tmp_path / "batches")
    monkeypatch.setattr(uygulama, "SEQUENCE_PATH", tmp_path / "sequence.json")
    client = uygulama.app.test_client()
    assert client.post("/batch/create", data={"count": "20", "fill_rate": "85", "test_count": "4"}).status_code == 200
    batch = next((tmp_path / "batches").iterdir())
    dosyalar = sorted(p.name for p in (batch / "ocr_ground_truth").iterdir())
    assert dosyalar[0] == "sfg00001.json" and len(dosyalar) == 20
    meta = json.loads((batch / "ground_truth.json").read_text(encoding="utf-8"))["metadata"]
    assert len(meta["test_form_ids"]) == 4
    kartlar = client.get(f"/batch/{batch.name}/cards").get_data(as_text=True)
    assert kartlar.count("TEST SETİ") == 8  # 4 form × 2 kart sayfası
    assert "Hayır'ı daire içine al" in kartlar
    assert client.post("/batch/create", data={"count": "5", "test_count": "5"}).status_code == 400
