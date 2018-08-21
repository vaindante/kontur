from itertools import zip_longest

import allure

from exceptions import MismatchError
from logger import logger


class CompareJson:
    start_index = 0
    accuracy = 3

    @staticmethod
    def is_instance(v_iter, v_type):
        return all(map(lambda t: isinstance(t, v_type), v_iter))

    def __call__(self, v_in, v_out):
        self.v_in = v_in if not isinstance(v_in, str) else v_in.strip()

        if isinstance(v_out, str):
            v_out = v_out.strip()

        mismatch_items = dict()
        if v_in == '!not_empty' and (v_out and 'нет в ответе' not in v_out if isinstance(v_out, str) else True):
            pass
        elif v_in == '!empty' and not v_out:
            pass
        elif self.v_in != v_out:
            # Сначала проверяем что пришел не список или другой попхожий итератор
            if self.is_instance((self.v_in, v_out), (list, tuple, map)):
                for key, value in enumerate(zip_longest(self.v_in, v_out), start=self.start_index):
                    result = CompareJson()(*value)
                    if result:
                        mismatch_items[key] = result

            elif isinstance(self.v_in, set):
                if self.v_in.symmetric_difference(v_out):
                    return self.formation_error(list(self.v_in), v_out)
                return

            elif self.is_instance((self.v_in, v_out), (int, float)):
                if round(self.v_in, self.accuracy) != round(v_out, self.accuracy):
                    return self.formation_error(self.v_in, v_out)
                return

            elif self.is_instance((self.v_in, v_out), dict):
                for key, value_in in self.v_in.items():
                    result = CompareJson()(
                        value_in,
                        v_out.get(key, 'Поля %r нет в ответе' % key)
                    )
                    if result:
                        mismatch_items[key] = result
            else:
                return self.formation_error(self.v_in, v_out)

            return mismatch_items

    @staticmethod
    def formation_error(v_in, v_out):
        return {
            'Хотели': v_in,
            'Получили': v_out
        }


#####################
def correspond_selected_object(objects, table):
    """
    Функция для проверки сравневания двух джисоно валидных объектов

    :param objects: объет который проверяем, может быть типа list или dict
    :param table: объект по которому проверяем objects, может иметь меньше значений чем objects, если проверям list,
                  предпочительнее скидывать tuple (шаблон, таблица; то, как должно быть)
    :return: None или error
    """

    with allure.step('Сравниваем данные с ожидаемыми значениями'):
        error = CompareJson()(
            table,
            objects
        )
        if error:
            logger.attach_debug('Данные которые проверяем', objects)
            logger.attach_debug('Данные для проверки', table)
            raise MismatchError('Данные не сошлись', error)
