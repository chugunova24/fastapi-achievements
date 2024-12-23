import pytest

from tests.conftest import settings, client


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_response",
    [
        (
            {"name": "Alice", "language": "en"},
            201,
            {"name": "Alice", "language": "en"}
        ),
        (
            {"name": "Bob", "language": "fr"}, # Доступны только языки en/ru
            422,
            None
        ),
        (
            {"name": "", "language": "en"},
            422,
            None  # Ожидаем ошибку валидации
        ),
        (
            {"name": "Charlie"},  # Отсутствует поле "language"
            201,
            {"name": "Charlie", "language": "en"}
        ),
    ]
)
def test_create_user(
        user_data,
        expected_status_code,
        expected_response
):
    # Отправляем POST запрос для создания пользователя
    response = client.post(
        settings.api_v1_prefix + "/users",
        json=user_data
    )

    # Проверяем статус ответа
    assert response.status_code == expected_status_code

    if expected_status_code == 201:
        result = response.json()
        del result["id"]
        assert result == expected_response
    else:
        # Если ожидается ошибка, проверяем, что тело ответа не
        # соответствует успешному результату
        assert "id" not in response.json()