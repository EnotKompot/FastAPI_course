async def test_facilities_api(ac):
    url = "/facilities"
    # Добавляем удобство
    request_add = await ac.post(url=url, json={"name": "Интернет"})
    assert request_add.status_code == 200

    # Получаем все удобства
    response1 = await ac.get(
        url=url,
    )
    assert response1.status_code == 200

    # Получаем последнее добавленное удобство по id
    last_facility_id = response1.json()[-1].get("id")
    response2 = await ac.get(
        url=f"{url}/{last_facility_id}",
    )
    assert response2.status_code == 200
