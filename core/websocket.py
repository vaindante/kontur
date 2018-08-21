import json
import threading
from time import time

import allure
from ws4py.client.threadedclient import WebSocketClient

from logger import logger


# from steps.rest_utils import check_response


class WSListener(threading.Thread):
    def __init__(self, url, session):
        super().__init__()

        self.url = url
        self.session = session
        self.ssid = session.ssid

        self.ws = self.WSClient(self.url, self.ssid, listener=self)
        self.message_list = list()

        self._is_stopped = True
        self._stop = threading.Event()
        self.daemon = True

    def __restart_connection(self):
        self.ws.close()

        del self.ws
        self.ws = self.WSClient(self.url, self.ssid, listener=self)

    ####################################################################################################################

    class WSClient(WebSocketClient):
        def __init__(self, url, ssid, listener):
            headers = [('Cookie', 'ssid=%s' % ssid)]
            super().__init__(url, headers=headers)

            self.listener = listener

        def received_message(self, message):
            try:
                msg_decode = json.loads(message.data.decode('utf-8'))
                self.listener.message_list.append(msg_decode)
                logger.info('### WS: get message: %r' % msg_decode)

            except (TypeError, json.decoder.JSONDecodeError):
                logger.warning('!!! WS: received message is not json: %r' % message.data)

    ####################################################################################################################

    def stop(self):
        self._is_stopped = True
        try:
            self.ws.close()
        except OSError:
            pass

    def restart(self):
        self.stop()
        self.__restart_connection()
        self.start()

    ####################################################################################################################
    @allure.step('Отправляем сообщение {1} по веб сокету')
    def send(self, query, *args):
        return self.ws.send(query, *args)

    @allure.step('Очищаем список сообщений ранее полученных по веб сокету')
    def clear_message_list(self):
        self.message_list = list()

    @allure.step('Возвращаем список сообщений полученых по веб сокету')
    def get_message_list(self):
        return self.message_list

    @allure.step('Ожидаем сообщений по веб сокету')
    def waiting_messages(self):
        start_time = time()
        while time() - start_time < 30:
            if self.message_list:
                return
        else:
            self.stop()
            raise TimeoutError('Сообщение от веб-сокета не было получено в течении 30 сек.')

    ####################################################################################################################

    def run(self):
        self._is_stopped = False
        need_ws_reconnect = False
        ws_fail_count = 0

        while not self._is_stopped:
            try:
                self.ws.connect()
                self.ws.run_forever()

            except AttributeError:
                ws_fail_count += 1
                logger.warning('!!! WS: Thread is down... restarting: %s' % ws_fail_count)

                self._is_stopped = True
                need_ws_reconnect = True

            finally:
                self.ws.close()

            if need_ws_reconnect:
                if ws_fail_count > 10:
                    logger.warning('!!! WS: Terminate thread after 10 reconnect attempts')
                    break
                else:
                    self.__restart_connection()
                    need_ws_reconnect = False
