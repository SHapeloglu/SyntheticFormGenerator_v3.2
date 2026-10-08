import app as uygulama


def test_onizleme_route(tmp_path, monkeypatch):
    monkeypatch.setattr(uygulama, "BATCH_DIR", tmp_path / "batches")
    monkeypatch.setattr(uygulama, "SEQUENCE_PATH", tmp_path / "sequence.json")
    client = uygulama.app.test_client()
    assert client.post("/batch/create", data={"count": "2", "fill_rate": "100"}).status_code == 200
    batch_id = next((tmp_path / "batches").iterdir()).name

    yanit = client.get(f"/batch/{batch_id}/preview/FORM-00001/page1")
    assert yanit.status_code == 200
    assert yanit.mimetype == "image/jpeg"
    assert client.get(f"/batch/{batch_id}/preview/FORM-99999/page1").status_code == 404
    assert client.get(f"/batch/{batch_id}/preview/FORM-00001/page9").status_code == 404
