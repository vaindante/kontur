from time import sleep

import pytest


@pytest.allure.story('Проверяем что удалось авторизоваться и нам приходят сообщения раз в секунду')
@pytest.mark.test
def test_test(ws):
    ws.clear_message_list()
    sleep(10)
    mes_list = [v['msg'] for v in ws.get_message_list() if v['name'] == 'timeSync']
    with pytest.allure.step('Проверяем что между полученными сообщениями прошла 1 секунда'):
        assert all(round(v / 1000, 0) == -1 for v in (v1 - v2 for v1, v2 in zip(mes_list, mes_list[1:])))


@pytest.allure.story('Проверяем что вебсокет умеет принимать собщения с разными символами')
@pytest.mark.parametrize('query', ('Тест', 'Test', 'փորձարկում', 'ሙከራ', 'δοκιμή', 'テスト'))
@pytest.mark.test
def test_send_messege(ws, query):
    ws.send(query)

    # очищаем список от сообщений
    ws.clear_message_list()
    # Проверяем что сообщения еще приходят
    ws.waiting_messages()


@pytest.allure.story('Пробуем авторизоваться под не зарегистрированным пользователем')
@pytest.mark.test
def test_rest(rest):
    with pytest.raises(ConnectionError):
        rest.auth_in_back_office('test@test.com')
