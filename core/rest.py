from json import dumps

import requests

from exceptions import ResponseException


class RestApiForBack:
    def __init__(self, host, user, token, repos):
        # Авторизация
        self.host, self.repos = host, repos
        self.session = requests.session()
        self.session.auth = (user, token)
        self.login = self.get(f'{host}/user')['login']
        self.url = f"{self.host}/repos/{self.login}/{self.repos}/issues"

    @staticmethod
    def check_status_code(status_code, need_status_code):
        if status_code != need_status_code:
            raise Exception('Код состояния HTTP запроса должен быть %s, а сейчас %s' % (need_status_code, status_code))

    # Свойтсва класса ##################################################################################################

    # Запрос #################################################################################################
    def get(self, url, data=None, params=None):
        res = self.session.get(url, data=data, params=params)
        if res.status_code in [200, 201, 202, 204]:
            return res.json()
        else:
            raise ResponseException(res.text)

    def post(self, url, data=None, params=None):
        return self.session.post(url, data=data, params=params).json()

    def create_issue(self, data):
        return self.post(self.url, data=dumps(data))

    def get_issue_list(self):
        return self.get(self.url)

    def lock_issue(self, _id, comment="too heated"):
        return self.session.put(
            f'{self.url}/{_id}/lock',
            dumps(
                {
                    "locked": True,
                    "active_lock_reason": comment
                }
            )
        ).json()

    def edit_issue(self, _id, data):
        return self.session.patch(f'{self.url}/{_id}', dumps(data)).json()
