import pytest
import requests


class RestApiForBack:
    def __init__(self, url, login, passwd, *args, **kwargs):
        # Авторизация
        self._default_connect = self.current_connect = self.get_rest_session(url, login, passwd)
        self._reset_params()

    @pytest.allure.step('Авторизуемся под пользователем {1!r}')
    def auth_in_back_office(self, login, passwd='test'):
        self.current_connect = self.get_rest_session(self.url, login, passwd)
        return self

    @staticmethod
    def check_status_code(status_code, need_status_code):
        if status_code != need_status_code:
            raise Exception('Код состояния HTTP запроса должен быть %s, а сейчас %s' % (need_status_code, status_code))

    # Свойтсва класса ##################################################################################################
    @property
    def connect(self):
        return self.current_connect

    @connect.setter
    def connect(self, conn):
        if conn == 'default':
            self.current_connect = self._default_connect
        else:
            self.current_connect = conn

    @property
    def url(self):
        return self.current_connect.url

    @property
    def ssid(self):
        return self.current_connect.ssid

    # Запрос #################################################################################################
    def _reset_params(self):
        self.request_params = {}
        self.data = dict()

    # Get REST session
    @staticmethod
    def get_rest_session(url, email, passwd):
        # Auth in BackOffice
        auth_data = {"email": email, "password": passwd}

        # Create authenticated session for REST client
        session = requests.session()
        response = session.post(f'{url}/login', auth_data)

        # Сохраняем информацию по авторизации под кем мы авторизовались
        setattr(session, 'url', url)
        setattr(session, 'email', email)
        setattr(session, 'passwd', passwd)
        setattr(session, 'ssid', session.cookies.get_dict().get("ssid"))

        # Check status of AUTH in created session
        if response.status_code != 200:
            raise ConnectionError('HTTP AUTH Error %r. Status code: %s' % (f'{url}/login', response.status_code))
        else:
            return session
