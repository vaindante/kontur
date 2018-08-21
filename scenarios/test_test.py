from time import sleep

import pytest

from utils import correspond_selected_object


@pytest.allure.story('Проверяем что удалось авторизоваться и нам приходят сообщения раз в секунду')
@pytest.mark.test
@pytest.mark.test_1
def test_test(ws):
    ws.clear_message_list()
    sleep(10)
    mes_list = [v['msg'] for v in ws.get_message_list() if v['name'] == 'timeSync']
    with pytest.allure.step('Проверяем что между полученными сообщениями прошла 1 секунда'):
        assert all(round(v / 1000, 0) == -1 for v in (v1 - v2 for v1, v2 in zip(mes_list, mes_list[1:])))


@pytest.allure.story('Проверяем что вебсокет умеет принимать собщения с разными символами')
@pytest.mark.parametrize('query', ('Тест', 'Test', 'փորձարկում', 'ሙከራ', 'δοκιμή', 'テスト'))
@pytest.mark.test
@pytest.mark.test_2
def test_send_messege(ws, query):
    ws.send(query)

    # очищаем список от сообщений
    ws.clear_message_list()
    # Проверяем что сообщения еще приходят
    ws.waiting_messages()


@pytest.allure.story('Пробуем авторизоваться под не зарегистрированным пользователем')
@pytest.mark.test
@pytest.mark.test_3
def test_rest(rest):
    with pytest.raises(ConnectionError):
        rest.auth_in_back_office('test@test.com')


@pytest.allure.story('Проверяем что при авторизации пришло сообщение с профилем')
@pytest.mark.test
@pytest.mark.test_4
def test_check_profile(ws):
    ws.waiting_messages()
    for mes in ws.get_message_list():
        if mes.get('name') == 'profile':
            correspond_selected_object(
                mes.get('msg'),
                {
                    'balance': 10000.0,
                    'balances': '!not_empty',
                    'country_id': 206,
                    'currency': 'USD',
                    'email': 'hed01351@bnuis.com',
                    'name': 'Test Testing',
                }
            )
            break
        else:
            assert True, 'Не найдено сообщение с профилем'


@pytest.allure.story('Проверяем что при авторизации c левым ssid не возможна')
@pytest.mark.test
@pytest.mark.test_5
def test_check_profile(ws):
    ws.waiting_messages()
    with pytest.allure.step('Пробуем авторизоваться'):
        with pytest.raises(RuntimeError):
            ws.restart(ssid='1341234')
