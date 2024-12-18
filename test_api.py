import json
import os
import uuid

import pytest
from pytest_httpx import HTTPXMock

from py3xui import AsyncApi, Client, Inbound
from py3xui.inbound import Settings, Sniffing, StreamSettings

RESPONSES_DIR = os.path.join(os.path.dirname(__file__), "responses")
HOST = "http://localhost"
USERNAME = "admin"
PASSWORD = "admin"
SESSION = "abc123"
EMAIL = "alhtim2x"


@pytest.mark.asyncio
async def test_get_client(httpx_mock: HTTPXMock):
    """
    Тестирует получение клиента по его email.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен,
    и что возвращаемый клиент соответствует ожидаемым значениям.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "get_client.json")))

    httpx_mock.add_response(
        method="GET",
        url=f"{HOST}/panel/api/inbounds/getClientTraffics/{EMAIL}",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    client = await api.client.get_by_email(EMAIL)

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"
    assert isinstance(client, Client), f"Ожидался Client, получен {type(client)}"
    assert client.email == EMAIL, f"Ожидалось {EMAIL}, получено {client.email}"
    assert client.id == 1, f"Ожидалось 1, получено {client.id}"


@pytest.mark.asyncio
async def test_get_ips(httpx_mock: HTTPXMock):
    """
    Тестирует получение IP-адресов клиента по его email.

    Использует мок для имитации ответа API. Проверяет, что возвращаемый список IP-адресов пуст.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True, "msg": "", "obj": "Нет записей IP"}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/clientIps/{EMAIL}",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    ips = await api.client.get_ips(EMAIL)

    assert ips == "Нет записей IP", f"Ожидалось 'Нет записей IP', получено {ips}"


@pytest.mark.asyncio
async def test_add_clients(httpx_mock: HTTPXMock):
    """
    Тестирует добавление нового клиента.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что клиент был успешно добавлен.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    client = Client(id=str(uuid.uuid4()), email="test", enable=True)
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/addClient",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.client.add(1, [client])

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_update_client(httpx_mock: HTTPXMock):
    """
    Тестирует обновление информации о клиенте.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что информация о клиенте была успешно обновлена.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    client = Client(id=str(uuid.uuid4()), email="test", enable=True)
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/updateClient/{client.id}",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.client.update(client.id, client)

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_reset_client_ips(httpx_mock: HTTPXMock):
    """
    Тестирует сброс IP-адресов клиента.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что IP-адреса клиента были успешно сброшены.

 :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/clearClientIps/{EMAIL}",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.client.reset_ips(EMAIL)

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_reset_client_stats(httpx_mock: HTTPXMock):
    """
    Тестирует сброс статистики клиента.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что статистика клиента была успешно сброшена.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/1/resetClientTraffic/{EMAIL}",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.client.reset_stats(1, EMAIL)

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_delete_client(httpx_mock: HTTPXMock):
    """
    Тестирует удаление клиента.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что клиент был успешно удален.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/1/delClient/1",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.client.delete(1, "1")

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_delete_depleted_clients(httpx_mock: HTTPXMock):
    """
    Тестирует удаление истощенных клиентов.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что истощенные клиенты были успешно удалены.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/delDepletedClients/1",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.client.delete_depleted(1)

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_client_online(httpx_mock: HTTPXMock):
    """
    Тестирует получение информации о клиентах, которые в данный момент онлайн.

    Использует мо к для имитации ответа API. Проверяет, что запрос был выполнен
    и что информация о клиентах онлайн была успешно получена.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/onlines",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.client.online()

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_get_client_traffic_by_id(httpx_mock: HTTPXMock):
    """
    Тестирует получение трафика клиента по его ID.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен,
    и что возвращаемый клиент соответствует ожидаемым значениям.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {
        "success": True,
        "msg": "",
        "obj": [
            {
                "id": 1,
                "inboundId": 1,
                "enable": True,
                "email": "test",
                "up": 170579,
                "down": 8995344,
                "expiryTime": 0,
                "total": 0,
                "reset": 0,
            }
        ],
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{HOST}/panel/api/inbounds/getClientTrafficsById/239708ef-487e-4945-829d-ad79a0ce067e",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION

    clients = await api.client.get_traffic_by_id("239708ef-487e-4945-829d-ad79a0ce067e")

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"
    assert len(clients) == 1, f"Ожидалось 1, получено {len(clients)}"

    client = clients[0]

    assert isinstance(client, Client), f"Ожидался Client, получен {type(client)}"
    assert client.email == "test", f"Ожидалось test, получено {client.email}"
    assert client.id == 1, f"Ожидалось 1, получено {client.id}"


def _prepare_inbound() -> Inbound:
    """
    Подготавливает объект Inbound с заданными настройками.

    :return: Экземпляр класса Inbound с предустановленными параметрами.
    """
    settings = Settings()
    sniffing = Sniffing(enabled=True)

    tcp_settings = {
        "acceptProxyProtocol": False,
        "header": {"type": "none"},
    }
    stream_settings = StreamSettings(security="reality", network="tcp", tcp_settings=tcp_settings)

    inbound = Inbound(
        enable=True,
        port=999,
        protocol="vless",
        settings=settings,
        stream_settings=stream_settings,
        sniffing=sniffing,
    )

    return inbound


@pytest.mark.asyncio
async def test_get_inbounds(httpx_mock: HTTPXMock):
    """
    Тестирует получение списка входящих соединений.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен,
    и что возвращаемый список входящих соединений соответствует ожидаемым значениям.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = json.load(open(os.path.join(RESPONSES_DIR, "get_inbounds.json")))

    httpx_mock.add_response(
        method="GET",
        url=f"{HOST}/panel/api/inbounds/list",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    inbounds = await api.inbound.get_list()

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"
    assert len(inbounds) == 1, f"Ожидалось 1, получено {len(inbounds)}"
    inbound = inbounds[0]
    assert isinstance(inbound, Inbound), f"Ожидался Inbound, получен {type(inbound)}"
    assert isinstance(
        inbound.stream_settings, (StreamSettings, str)
    ), f"Ожидалось StreamSettings или str, получено { type(inbound.stream_settings)}"

    assert isinstance(
        inbound.sniffing, Sniffing
    ), f"Ожидался Sniffing, получен {type(inbound.sniffing)}"
    assert isinstance(
        inbound.client_stats[0], Client
    ), f"Ожидался ClientStats, получен {type(inbound.client_stats[0])}"

    assert inbound.id == 1, f"Ожидалось 1, получено {inbound.id}"


@pytest.mark.asyncio
async def test_add_inbound(httpx_mock: HTTPXMock):
    """
    Тестирует добавление нового входящего соединения.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что входящее соединение было успешно добавлено.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/add",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.inbound.add(_prepare_inbound())

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_delete_inbound_success(httpx_mock: HTTPXMock):
    """
    Тестирует успешное удаление входящего соединения.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что входящее соединение было успешно удалено.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/del/1",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.inbound.delete(1)

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_delete_inbound_failed(httpx_mock: HTTPXMock):
    """
    Тестирует неудачное удаление входящего соединения.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что при попытке удалить несуществующее соединение возникает ошибка.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": False, "msg": "Ошибка удаления: запись не найдена"}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/del/1",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    with pytest.raises(ValueError):
        await api.inbound.delete(1)

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_update_inbound(httpx_mock: HTTPXMock):
    """
    Тестирует обновление входящего соединения.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что входящее соединение было успешно обновлено.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="POST",
        url=f"{HOST}/panel/api/inbounds/update/1",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.inbound.update(1, _prepare_inbound())

    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"


@pytest.mark.asyncio
async def test_database_export(httpx_mock: HTTPXMock):
    """
    Тестирует экспорт базы данных.

    Использует мок для имитации ответа API. Проверяет, что запрос был выполнен
    и что база данных была успешно экспортирована.

    :param httpx_mock: Мок для HTTP-запросов.
    """
    response_example = {"success": True}

    httpx_mock.add_response(
        method="GET",
        url=f"{HOST}/panel/api/inbounds/createbackup",
        json=response_example,
        status_code=200,
    )

    api = AsyncApi(HOST, USERNAME, PASSWORD)
    api.session = SESSION
    await api.database.export()
    assert httpx_mock.get_request(), "Замеченный запрос не был вызван"