"""Mocked bot."""
from collections import deque
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Any

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Request, Response, TelegramType
from aiogram.types import ResponseParameters, User
from aiogram.types.base import UNSET


class MockedSession(BaseSession):
    """Mocked session for tests."""

    def __init__(self):
        """Mocked session is used for offline integration tests."""
        super().__init__()
        self.responses: deque[Response[TelegramType]] = deque()
        self.requests: deque[Request] = deque()
        self.closed = True

    def add_result(
        self, response: Response[TelegramType]
    ) -> Response[TelegramType]:
        """Mocked method for add result.

        :param response: Response to add
        :return: this Response.
        """
        self.responses.append(response)
        return response

    def get_request(self) -> Request:
        """Mocked method for get request.

        :return: Request.
        """
        return self.requests.pop()

    async def close(self):
        """Mocked method for closing the session.

        :return: Nothing.
        """
        self.closed = True

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = UNSET,
    ) -> TelegramType:
        """Build request and get response.

        :param bot: Bot instance which used for request
        :param method: method to make request
        :param timeout: Timeout when request is need to be aborted
        :return: The Result of request.
        """
        self.closed = False
        self.requests.append(method.build_request(bot))
        try:
            response: Response[TelegramType] = self.responses.pop()
        except IndexError:
            return method
        else:
            self.check_response(
                method=method,
                status_code=response.error_code,
                content=response.model_dump('json'),
            )
            return response.result  # type: ignore

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        """Just mocked and shutted down method."""
        yield b''


class MockedBot(Bot):
    """Mocked bot for tests."""

    if TYPE_CHECKING:
        session: MockedSession

    def __init__(self, **kwargs):
        """Mocked session init."""
        super().__init__(
            kwargs.pop('token', '42:TEST'), session=MockedSession(), **kwargs
        )
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name='FirstName',
            last_name='LastName',
            username='tbot',
            language_code='uk-UA',
        )

    def add_result_for(
        self,
        method: type[TelegramMethod[TelegramType]],
        ok: bool,
        result: TelegramType = None,
        description: str | None = None,
        error_code: int = 200,
        migrate_to_chat_id: int | None = None,
        retry_after: int | None = None,
    ) -> Response[TelegramType]:
        """The mocked add_result_for function adds a result to the session.

        :param self: Access the class instance
        :param method: Get the return type of the method
        :param ok: Indicate whether the request was successful or not
        :param result: Define the type of the result
        :param description: Provide a description of the result
        :param error_code: Indicate that the request was successful
        :param migrate_to_chat_id: Migrate to chat update
        :param retry_after: Specify the time to wait before a request can be repeated
        :return: A response object, which is a subclass of namedtuple
        :doc-author: Trelent.
        """
        response = Response[method.__returning__](  # type: ignore
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            parameters=ResponseParameters(
                migrate_to_chat_id=migrate_to_chat_id,
                retry_after=retry_after,
            ),
        )
        self.session.add_result(response)
        return response

    def get_request(self) -> Request:
        """Get last request.

        The get_request function returns a Request object that has been created
        by the Session object. The get_request function is called when the user
        wants to make a request to an endpoint.

        :param self: Access the class attributes and methods
        :return: A request object
        :doc-author: Trelent.
        """
        return self.session.get_request()
