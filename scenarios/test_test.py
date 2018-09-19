from itertools import combinations
from uuid import uuid4

import pytest
from loremipsum import get_sentence

from utils import correspond_selected_object

test_data_2 = {
    "title": get_sentence(),
    "body": get_sentence(),
    "labels": ["bug", 'fix']
}
test_data_1 = {
    "state": "open",
    **test_data_2
}

test_data_3 = test_data_1


@pytest.allure.story('Проверяем что удалось авторизоваться и мы получаем список "issues"')
@pytest.mark.test
@pytest.mark.test_1
def test_test_1(rest):
    rest.get_issue_list()


@pytest.allure.story('Проверяем что можем создать и редактировать "issues"')
@pytest.mark.test
@pytest.mark.test_2
@pytest.mark.parametrize('keys', combinations(test_data_1, 2))
def test_test_2(rest, keys):
    data = {k: test_data_1[k] for k in keys}
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


@pytest.allure.story('Проверяем что можем редактировать "issues" со статусом "closed"')
@pytest.mark.test
@pytest.mark.test_3
@pytest.mark.parametrize('keys', combinations(test_data_2, 2))
def test_test_3(rest, keys):
    data = {k: test_data_2[k] for k in keys}
    with pytest.allure.step('Создаем issue'):
        number = rest.create_issue(
            {
                'title': str(uuid4()),
                'body': 'test'
            }
        )['number']
        rest.edit_issue(number, {"state": "closed"})

    with pytest.allure.step('Редактируем'):
        issue_edit = rest.edit_issue(number, data)
        if 'labels' in keys:
            data = {**data, "labels": [{"name": "bug"}, {"name": "fix"}]}

    with pytest.allure.step('проверяем ответ'):
        correspond_selected_object(issue_edit, data)


@pytest.allure.story('Проверяем что можем очистить "labels"')
@pytest.mark.test
@pytest.mark.test_4
def test_test_4(rest):
    with pytest.allure.step('Создаем issue'):
        number = rest.create_issue(
            {
                'title': str(uuid4()),
                'body': 'test'
            }
        )['number']

    with pytest.allure.step('Редактируем'):
        rest.edit_issue(number, {"labels": ["bug", 'fix']})
        issue_edit = rest.edit_issue(number, {"labels": []})

    with pytest.allure.step('проверяем ответ'):
        correspond_selected_object(issue_edit, {"labels": []})

    rest.edit_issue(number, {"state": "closed"})


@pytest.allure.story('Проверяем что можем редактировать "issues" со статусом "lock "')
@pytest.mark.test
@pytest.mark.test_5
@pytest.mark.parametrize('keys', combinations(test_data_3, 2))
def test_test_5(rest, keys):
    data = {k: test_data_3[k] for k in keys}
    with pytest.allure.step('Создаем issue'):
        number = rest.create_issue(
            {
                'title': str(uuid4()),
                'body': 'test'
            }
        )['number']
        rest.lock_issue(number)

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
