from services.data_generator import generate_records, synthetic_tc


def tc_gecerli_mi(tc: str) -> bool:
    """T.C. kimlik no kurallarının üretim kodundan bağımsız kontrolü."""
    if len(tc) != 11 or not tc.isdigit() or tc[0] == "0":
        return False
    d = [int(c) for c in tc]
    tek = d[0] + d[2] + d[4] + d[6] + d[8]
    cift = d[1] + d[3] + d[5] + d[7]
    if (tek * 7 - cift) % 10 != d[9]:
        return False
    return sum(d[:10]) % 10 == d[10]


def test_ornek_numaralar_gecerli():
    for index in (0, 1, 2, 9, 10, 99, 12_345, 99_999, 999_999):
        assert tc_gecerli_mi(synthetic_tc(index)), index


def test_aralik_boyunca_gecerli_ve_benzersiz():
    numaralar = [synthetic_tc(i) for i in range(1, 5001)]
    assert all(tc_gecerli_mi(n) for n in numaralar)
    assert len(set(numaralar)) == len(numaralar)


def test_bozuk_numarayi_kontrol_yakalar():
    tc = synthetic_tc(42)
    bozuk = tc[:10] + str((int(tc[10]) + 1) % 10)
    assert not tc_gecerli_mi(bozuk)


def test_uretilen_kayitlarda_tc_gecerli():
    for record in generate_records(count=20, fill_rate=100, start_index=500):
        tc = str(record.get("T.C. Kimlik No", ""))
        if tc:
            assert tc_gecerli_mi(tc), tc
