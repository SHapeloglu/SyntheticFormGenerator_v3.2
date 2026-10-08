import json
import threading

import pytest

from services.sequence_manager import reserve_sequence


def test_dosya_yoksa_birden_baslar(tmp_path):
    path = tmp_path / "sequence.json"
    assert reserve_sequence(path, 5) == 1
    assert json.loads(path.read_text(encoding="utf-8")) == {"next_form_number": 6}
    assert reserve_sequence(path, 3) == 6


def test_gecersiz_sayi_reddedilir(tmp_path):
    path = tmp_path / "sequence.json"
    with pytest.raises(ValueError):
        reserve_sequence(path, 0)
    assert not path.exists()


def test_eszamanli_rezervasyonlar_cakismaz(tmp_path):
    path = tmp_path / "sequence.json"
    adet, is_parcacigi = 7, 40
    baslangiclar: list[int] = []
    kilit = threading.Lock()
    engel = threading.Barrier(is_parcacigi)

    def calis():
        engel.wait()
        baslangic = reserve_sequence(path, adet)
        with kilit:
            baslangiclar.append(baslangic)

    threads = [threading.Thread(target=calis) for _ in range(is_parcacigi)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    numaralar = [b + i for b in baslangiclar for i in range(adet)]
    assert sorted(numaralar) == list(range(1, adet * is_parcacigi + 1))
    assert json.loads(path.read_text(encoding="utf-8"))["next_form_number"] == adet * is_parcacigi + 1
