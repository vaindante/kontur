from itertools import combinations
from uuid import uuid4

import pytest
from loremipsum import get_sentence

from utils import correspond_selected_object

test_data = {
    "title": get_sentence(),
    "body": get_sentence(),
    "state": "open",
    "labels": ["bug", 'fix']
}


@pytest.allure.story('Проверяем что удалось авторизоваться и мы получаем список "issues"')
@pytest.mark.test
@pytest.mark.test_1
def test_test_1(rest):
    assert rest.get_issue_list()


@pytest.allure.story('Проверяем что можем создать и редактировать "issues"')
@pytest.mark.test
@pytest.mark.test_2
@pytest.mark.parametrize('keys', combinations(test_data, 2))
def test_test_2(rest, keys):
    data = {k: test_data[k] for k in keys}
    with pytest.allure.step('Создаем issue'):
        number = rest.create_issue(
            {
                'title': str(uuid4()),
                'body': 'test'
            }
        )['number']
    with pytest.allure.step('Редактируем'):
        issue_edit = rest.edit_issue(number, data)
        if 'labels' in keys:
            data = {**data, "labels": [{"name": "bug"}, {"name": "fix"}]}

    with pytest.allure.step('проверяем ответ'):
        correspond_selected_object(issue_edit, data)

    with pytest.allure.step('проверяем измения на сайте'):
        correspond_selected_object(
            list(filter(lambda x: x['number'] == number, rest.get_issue_list()))[0],
            data
        )

    rest.edit_issue(number, {"state": "closed"})
