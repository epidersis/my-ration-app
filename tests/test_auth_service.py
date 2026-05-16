from app.services.auth_service import verify_password


def test_verify_password_rejects_malformed_hash() -> None:
    assert not verify_password("secret", "pbkdf2_sha256$260000$abc$abc")
