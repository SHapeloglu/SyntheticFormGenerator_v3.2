"""Başlangıç ekranı: hata sonrası girilen değerler korunur, sıradaki numara gösterilir, sayaç yazmadan okunur.
Sayaç dosyası geçici bir kopyaya yönlendirilir: bu testler gerçek config/sequence.json'u ASLA değiştirmez; parti üretmez."""
import json

import pytest

import app as uygulama
from services.sequence_manager import peek_sequence


@pytest.fixture()
def sayac(tmp_path, monkeypatch):
    yol = tmp_path / "sequence.json"
    yol.write_text(json.dumps({"next_form_number": 77}), encoding="utf-8")
    monkeypatch.setattr(uygulama, "SEQUENCE_PATH", yol)
    return yol


def test_peek_yazmaz_ve_bozuk_dosyada_1_doner(tmp_path):
    yok = tmp_path / "yok" / "sequence.json"
    assert peek_sequence(yok) == 1 and not yok.exists() and not yok.parent.exists()
    bozuk = tmp_path / "bozuk.json"
    bozuk.write_text("{bozuk", encoding="utf-8")
    assert peek_sequence(bozuk) == 1
    iyi = tmp_path / "iyi.json"
    iyi.write_text(json.dumps({"next_form_number": 121}), encoding="utf-8")
    once = iyi.read_text(encoding="utf-8")
    assert peek_sequence(iyi) == 121 and iyi.read_text(encoding="utf-8") == once


def test_varsayilanlar_ve_siradaki_numara(sayac):
    html = uygulama.app.test_client().get("/").get_data(as_text=True)
    assert 'name="count" type="number" min="1" max="500" value="50"' in html
    assert 'name="test_count" type="number" min="0" max="100" value="10"' in html
    for secili in ('<option value="random" selected>', '<option value="85" selected>', '<option value="10" selected>'):
        assert secili in html, secili
    assert "var sonraki = 77;" in html


def test_hata_sonrasi_degerler_korunur_ve_sayac_degismez(sayac):
    once = sayac.read_text(encoding="utf-8")
    yanit = uygulama.app.test_client().post("/batch/create", data={
        "count": "10", "test_count": "10", "doctor_profile": "minimal", "fill_rate": "100", "repeat_rate": "0"})
    html = yanit.get_data(as_text=True)
    assert yanit.status_code == 400
    assert "0 ile toplamın bir eksiği" in html
    assert 'name="count" type="number" min="1" max="500" value="10"' in html          # 50'ye dönmemeli
    assert 'name="test_count" type="number" min="0" max="100" value="10"' in html
    for secili in ('<option value="minimal" selected>', '<option value="100" selected>', '<option value="0" selected>'):
        assert secili in html, secili
    assert '<option value="random" selected>' not in html
    assert sayac.read_text(encoding="utf-8") == once                                 # hata numara tüketmez


def test_onay_betigi_bagli(sayac):
    html = uygulama.app.test_client().get("/").get_data(as_text=True)
    assert "confirm(" in html
    assert "Form numaraları" in html
    assert "t >= c" in html
