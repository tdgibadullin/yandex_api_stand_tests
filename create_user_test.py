# Импортируем модуль sender_stand_request,
# содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request

# Импортируем модуль data, в котором определены данные,
# необходимые для HTTP-запросов.
import data

# Функция для замены значения в параметре firstName в теле запроса.
def get_user_body(first_name):
    # Копирование словаря с телом запроса из файла data.
    current_body = data.user_body.copy()
    # Изменение значения в поле firstName.
    current_body["firstName"] = first_name
    # Возвращается новый словарь с нужным значением firstName.
    return current_body

# Функция для позитивных проверок.
def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса.
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса
    # на создание пользователя.
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201.
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое.
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса
    # на получение данных из таблицы user_model.
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе.
    str_user = (user_body["firstName"] + ","
                + user_body["phone"] + ","
                + user_body["address"] + ",,,"
                + user_response.json()["authToken"])

    # Проверка, что такой пользователь есть и он единственный.
    assert users_table_response.text.count(str_user) == 1

# Функция для негативных проверок (символы).
def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса.
    user_body = get_user_body(first_name)

    # В переменную response сохраняется результат запроса
    # на создание пользователя.
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400.
    assert response.status_code == 400

    # Проверяется, что в теле ответа атрибут "code" равен 400.
    assert response.json()["code"] == 400
    # Проверяется текст в теле ответа в атрибуте "message".
    assert response.json()["message"] == ("Имя пользователя введено "
                                          "некорректно. Имя может содержать "
                                          "только русские или латинские "
                                          "буквы, длина должна быть не менее "
                                          "2 и не более 15 символов")

# Функция для негативных проверок
# (отсутствие параметра или пустой параметр).
def negative_assert_no_firstname(user_body):
    # В переменную response сохраняется результат запроса
    # на создание пользователя.
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400.
    assert response.status_code == 400

    # Проверяется, что в теле ответа атрибут "code" равен 400.
    assert response.json()["code"] == 400
    # Проверяется текст в теле ответа в атрибуте "message".
    assert response.json()["message"] == ("Не все необходимые параметры "
                                          "были переданы")

# Тест 1. Успешное создание пользователя
# (параметр firstName состоит из 2 символов).
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Аа")

# Тест 2. Успешное создание пользователя
# (параметр firstName состоит из 15 символов).
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

# Тест 3. Ошибка
# (параметр firstName состоит из 1 символа).
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")

# Тест 4. Ошибка
# (параметр firstName состоит из 16 символов).
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")

# Тест 5. Успешное создание пользователя
# (параметр firstName содержит английские буквы).
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Успешное создание пользователя
# (параметр firstName содержит русские буквы).
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 7. Ошибка
# (параметр firstName содержит пробел).
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")

# Тест 8. Ошибка
# (параметр firstName содержит спецсимволы).
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

# Тест 9. Ошибка
# (параметр firstName содержит цифры).
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Тест 10. Ошибка
# (в запросе нет параметра firstName)
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data
    # в переменную user_body.
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса.
    user_body.pop("firstName")
    # Проверка полученного ответа.
    negative_assert_no_firstname(user_body)

# Тест 11. Ошибка
# (параметр firstName состоит из пустой строки)
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса.
    user_body = get_user_body("")
    # Проверка полученного ответа.
    negative_assert_no_firstname(user_body)

# Тест 12. Ошибка
# (параметр firstName имеет другой тип (число)).
def test_create_user_number_type_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса.
    user_body = get_user_body(12)
    # В переменную response сохраняется результат запроса
    # на создание пользователя.
    response = sender_stand_request.post_new_user(user_body)

    # Проверка кода ответа.
    assert response.status_code == 400