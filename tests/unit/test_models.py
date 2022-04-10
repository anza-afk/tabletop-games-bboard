def test_new_user(new_user):
    """
    GIVEN модель польщователя
    WHEN создание нового пользователя
    THEN проверяет верность полей
    """

    assert new_user.username == 'test_user_01'
    assert new_user.email == 'testuser01@mail.ru'
    assert new_user.password != '00000'
