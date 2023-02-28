from collections import deque
from typing import TYPE_CHECKING, AsyncGenerator, Deque, Optional, Type

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Request, Response, TelegramType
from aiogram.types import UNSET, ResponseParameters, User


class MockedSession(BaseSession):
    """
    Mocked session for tests
    """

    def __init__(self):
        super(MockedSession, self).__init__()
        self.responses: Deque[Response[TelegramType]] = deque()
        self.requests: Deque[Request] = deque()
        self.closed = True

    def add_result(self, response: Response[TelegramType]) -> Response[TelegramType]:
        """
        Mocked method for add result
        :param response: Response to add
        :return: this Response
        """
        self.responses.append(response)
        return response

    def get_request(self) -> Request:
        """
        Mocked method for get request
        :return: Request
        """
        return self.requests.pop()

    async def close(self):
        """
        Mocked method for closing the session
        :return: Nothing
        """
        self.closed = True

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: Optional[int] = UNSET,
    ) -> TelegramType:
        """
        Build request and get response
        :param bot: Bot instance which used for request
        :param method: method to make request
        :param timeout: Timeout when request is need to be aborted
        :return: The Result of request
        """
        self.closed = False
        self.requests.append(method.build_request(bot))
        try:
            response: Response[TelegramType] = self.responses.pop()
        except IndexError:
            return method
        else:
            self.check_response(
                method=method, status_code=response.error_code, content=response.json()
            )
            return response.result  # type: ignore

    async def stream_content(
        self, url: str, timeout: int, chunk_size: int
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        """
        Just mocked and shutted down method
        """
        yield b""


class MockedBot(Bot):
    """
    Mocked bot for tests
    """

    if TYPE_CHECKING:
        session: MockedSession

    def __init__(self, **kwargs):
        super(MockedBot, self).__init__(
            kwargs.pop("token", "42:TEST"), session=MockedSession(), **kwargs
        )
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name="FirstName",
            last_name="LastName",
            username="tbot",
            language_code="uk-UA",
        )

    def add_result_for(
        self,
        method: Type[TelegramMethod[TelegramType]],
        ok: bool,
        result: TelegramType = None,
        description: Optional[str] = None,
        error_code: int = 200,
        migrate_to_chat_id: Optional[int] = None,
        retry_after: Optional[int] = None,
    ) -> Response[TelegramType]:
        """
        The mocked add_result_for function adds a result to the session.
        :param self: Access the class instance
        :param method:Type[TelegramMethod[TelegramType]]: Get the return type of the method
        :param ok:bool: Indicate whether the request was successful or not
        :param result:TelegramType=None: Define the type of the result
        :param description:Optional[str]=None: Provide a description of the result
        :param error_code:int=200: Indicate that the request was successful
        :param migrate_to_chat_id:Optional[int]=None: Indicate that the bot should be transferred to a different chat
        :param retry_after:Optional[int]=None: Specify the time to wait before a request can be repeated
        :param : Store the result of the request
        :return: A response object, which is a subclass of namedtuple
        :doc-author: Trelent
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
        """
        The get_request function returns a Request object that has been created by the Session object.
        The get_request function is called when the user wants to make a request to an endpoint.
        :param self: Access the class attributes and methods
        :return: A request object
        :doc-author: Trelent
        """

        return self.session.get_request()
