"""Alt yol (nginx X-Forwarded-Prefix) desteği: bütün bağlantılar öneki taşımalı, başlık yokken değişmemeli. Yalnız GET (parti üretmez)."""
import re

import app as uygulama

SAYFALAR = ["/", "/batches", "/search", "/coordinates"]
MUTLAK = re.compile(r"""(?:href|action|src)="(/[^"]*)"|fetch\(['"`](/[^'"`]*)|image\.src\s*=\s*`(/[^`]*)""")


def _al(yol, onek=None):
    istemci = uygulama.app.test_client()
    basliklar = {"X-Forwarded-Prefix": onek} if onek else {}
    return istemci.get(yol, headers=basliklar)


def test_onek_varken_tum_mutlak_baglantilar_onekli():
    for yol in SAYFALAR:
        yanit = _al(yol, "/sentetik")
        assert yanit.status_code == 200, yol
        metin = yanit.get_data(as_text=True)
        for m in MUTLAK.finditer(metin):
            hedef = next(g for g in m.groups() if g)
            assert hedef.startswith("/sentetik/") or hedef == "/sentetik", f"{yol}: önek yok -> {hedef}"


def test_onek_yokken_baglantilar_degismez():
    for yol in SAYFALAR:
        metin = _al(yol).get_data(as_text=True)
        assert "/sentetik" not in metin, yol
        assert 'href="/batches"' in _al("/").get_data(as_text=True)


def test_proxyfix_bagli():
    """Ara katman x_prefix=1 ile bağlı olmalı (test_client istekleri wsgi_app üzerinden geçer; yukarıdaki testler davranışı sınar)."""
    from werkzeug.middleware.proxy_fix import ProxyFix
    assert isinstance(uygulama.app.wsgi_app, ProxyFix)
    assert uygulama.app.wsgi_app.x_prefix == 1
