import os
import shutil
import subprocess
import threading

import pytest

from core import RestApiForBack
from env_config import cfg
from logger import logger


########################################################################################################################
# py.scenarios conf
def pytest_configure(config):
    logger.info('Start py.scenarios configuring')

    if os.getenv('GENERATE_REPORT', False):
        # Prepare reports dir
        reports_dir = 'reports'

        logger.info("delete report dir")

        try:
            shutil.rmtree(reports_dir)
            logger.info('  ... already deletes')
        except FileNotFoundError:
            pass
        finally:
            os.makedirs(reports_dir)
            logger.info('  ... create report dir')

    logger.info('Start executing:')


########################################################################################################################
@pytest.fixture(scope='session')
def rest():
    return RestApiForBack(
        host=cfg.host,
        user=cfg.user,
        token=cfg.token,
        repos=cfg.repos
    )


########################################################################################################################
# Hooks

# Called before fixtures
def pytest_runtest_setup(item):
    print('\n')
    threading.current_thread()._name = item.name

    # Очищаем ввывод логов для каждого теста, есть общие потоки, не получиться рестартовать логгер полностью
    logger.test_log.truncate(0)
    logger.test_log.seek(0)
    logger.info('==== Run fixtures ====:')


# Called to execute the scenarios item
def pytest_runtest_call(item):
    logger.info('=======================')
    logger.info('Run scenarios')


# After scenarios, before fixture ends
def pytest_runtest_teardown(item, nextitem):
    print('\n')
    logger.info('Stop scenarios')
    logger.info('==== Stop fixtures ====')


def pytest_runtest_makereport(item, call):
    # if scenarios result has fail
    if call.when == 'call':
        logger.attach_info('logs', logger.test_log.getvalue())


def pytest_unconfigure(config):
    # Для локальной ленивой генераци отчета.
    if os.getenv('GENERATE_REPORT', True):
        threading.current_thread()._name = 'Report'
        logger.info('### Create allure report ')
        try:
            subprocess.check_call('allure generate -c reports', shell=True)

        except subprocess.CalledProcessError:
            logger.warning('!!! allure: cannot create report - report dir is empty')
