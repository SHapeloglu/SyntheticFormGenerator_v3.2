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
            assert re.fullmatch(r"\d{2,3}", kayit["TA (tansiyon)"])
            assert re.fullmatch(r"\d{2,3}", kayit["TA diastolik kutusu"])  # mmHg kutusu artık dolu
            assert int(kayit["TA diastolik kutusu"]) < int(kayit["TA (tansiyon)"])
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
    assert "boş" in gt.values()
    assert gt["ta_diastolik"] != "boş"
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
    assert kartlar.count("TEST SETİ") == 4
    assert "Hayır'ı daire içine al" in kartlar
    assert client.post("/batch/create", data={"count": "5", "test_count": "5"}).status_code == 400


def test_kart_matbu_form_sirasinda():
    from services.data_generator import MATBU_SIRA
    assert [k for k, *_ in FORM_SCHEMA] == MATBU_SIRA


def test_tam_dolu_65_ile_100_arasi_rastgele_ve_bekar_cocuk_ve_kisa_ev_adresi():
    random.seed(11)
    kayitlar = generate_records(200, fill_rate=100)
    oranlar = []
    for kayit in kayitlar:
        dolu = sum(1 for _k, etiket, *_ in FORM_SCHEMA if kayit[etiket] != "")
        oranlar.append(dolu / len(FORM_SCHEMA))
        if kayit["Medeni Durumu"].startswith("Bek"):
            assert kayit["Soygeçmiş - Çocuk"] == ""
        assert kayit["TA diastolik kutusu"] != ""  # ölçümler boşaltılmaz
        assert not any(s in kayit["Ev Adresi"] for s in ("Sok", "Mah", "No:"))
    assert min(oranlar) >= 0.65
    assert max(oranlar) - min(oranlar) > 0.15  # her formda farklı doluluk



def test_anamnezde_nfm_yerine_tik_ve_n_da_var():
    random.seed(21)
    degerler = [k[e] for k in generate_records(200, fill_rate=100) for a, e, *_ in FORM_SCHEMA if a.startswith("anamnez")]
    assert degerler.count("NFM") > 0 and degerler.count("✓") > 0 and degerler.count("N") > 0
    random.seed(22)
    ham = [k[e] for k in generate_records(200, fill_rate=85) for a, e, *_ in FORM_SCHEMA if a.startswith("anamnez")]
    assert ham.count("NFM") / len(ham) > 0.3  # %85 modunda NFM baskın kalır


def test_ocr_ground_truth_tik_nfm_olur():
    kayit = generate_records(1, fill_rate=100)[0]
    etiket = next(e for a, e, *_ in FORM_SCHEMA if a == "anamnez1_carpinti")
    kayit[etiket] = "✓"
    assert ocr_ground_truth(kayit)["anamnez1_carpinti"] == "NFM"
