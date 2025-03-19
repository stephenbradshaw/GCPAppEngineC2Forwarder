import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get("/b8af860c6c7f78d5cbcaa86c8f11b268cd0c0295")
    assert r.status_code == 200
    assert "OK" in r.data.decode("utf-8")
