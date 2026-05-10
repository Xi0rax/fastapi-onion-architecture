from auth_service.src.security.jwt_utils import create_access_token, decode_access_token


def test_decode_access_token_returns_user_id():
    token = create_access_token("user-1")

    assert decode_access_token(token) == "user-1"
