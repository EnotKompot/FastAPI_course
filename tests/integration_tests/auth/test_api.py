import pytest

test_cases = {
    "params": "email, nickname, password, status_code",
    "values": [
        ("test1@mail.com", "test_user1", "12345", 200),
        ("test2@mail.ru", "test_user2", "1234", 200),
        ("test3@yandex.com", "test_user3", "123", 200),
        ("test1@mail.com", "test_user1", "12345", 409),
        ("test4@mailcom", "test_user4", "12345", 422),
        ("test5mail.com", "test_user5", "12345", 422),
        ("test6mailcom", "test_user6", "qwerty", 422),
        ("test7mail@.com", "test_user7", "password1", 422),
        ("test8.com", "test_user8", "QqWwEeRrTtYy", 422),
    ]
}

test_cases_validated = {
    "params": "email, nickname, password, status_code",
    "values": list(filter(lambda x: x[-1] == 200, test_cases["values"]))
}

@pytest.mark.parametrize(
    test_cases["params"],
    test_cases["values"]
)
async def test_user_register(
        ac,
        email, nickname, password, status_code,
):
    response = await ac.post(
        url="/auth/register",
        json={
            "email": email,
            "nickname": nickname,
            "password": password,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        answer = response.json()
        assert answer["success"] is True


@pytest.mark.parametrize(
    test_cases_validated["params"],
    test_cases_validated["values"]
)
async def test_user_login(
        ac,
        email, nickname, password, status_code,
):
    response = await ac.post(
        url="/auth/login",
        json={
            "email": email,
            "nickname": nickname,
            "password": password,

        }
    )
    assert response.status_code == status_code

    cookies = ""
    if status_code == 200:
        answer = response.json()
        cookies = response.cookies['access_token']
        assert cookies
        assert isinstance(cookies, str)
        assert answer["access_token"] == cookies
    return {"cookies": cookies}


@pytest.mark.parametrize(
    test_cases_validated["params"],
    test_cases_validated["values"]
)
async def test_get_userdata(
        ac,
        email, nickname, password, status_code,
):
    await test_user_login(ac, email, nickname, password, status_code)
    response = await ac.get(
        "/auth/me"
    )
    user_data = response.json()
    assert response.status_code == status_code
    if response.status_code == 200:
        assert user_data["email"] == email
        assert user_data["nickname"] == nickname
        assert "password" not in user_data
        assert "hashed_password" not in user_data


@pytest.mark.parametrize(
    test_cases_validated["params"],
    test_cases_validated["values"]
)
async def test_user_logout(
        ac,
        email, nickname, password, status_code,
):
    response = await test_user_login(ac, email, nickname, password, status_code)
    assert response.get("cookies") is not None # Checking that cookies exists after login
    response = await ac.get(
        "/auth/logout"
    )
    cookie = response.cookies
    assert "access token" not in cookie   # Checking that cookies is no more exist after logout


@pytest.mark.parametrize(
    test_cases_validated["params"],
    test_cases_validated["values"]
)
async def test_get_user_after_logout(
        ac,
        email, nickname, password, status_code,

):
    await test_user_login(ac, email, nickname, password, status_code)
    await ac.post("/auth/logout")
    response = await ac.get(
        "/auth/me"
    )
    assert response.status_code == 401