from typing import Any, Literal, overload, Union
import datetime

import requests

from edinet.enums.exceptions import (
    ResponseNot200,
    BadRequest,
    InvalidAPIKey,
    ResourceNotFound,
    InternalServerError
)
from edinet.enums.response import (
    GetDocumentResponse,
    GetDocumentResponseWithDocs
)

__all__ = ["Edinet"]


class Edinet:
    def __init__(self, token: str) -> None:
        """
        `token: str`
         APIのキー
        """
        # EDINET APIのバージョン(今のところ2しかないけど)
        EDINET_API_VERSION = 2
        # apiの保存
        self.__token = token
        # edinetAPIのURL
        self.__EDINET_URL = f"https://api.edinet-fsa.go.jp/api/v{EDINET_API_VERSION}/"

    def __request(self, endpoint: str, params: dict[str, Any]) -> requests.Response:
        """内部で使うrequestsメソッド、getリクエストのみ。"""

        params["Subscription-Key"] = self.__token

        res = requests.get(url=self.__EDINET_URL + endpoint,
                           params=params)

        if res.status_code == 200:
            return res
        elif res.status_code == 400:
            raise BadRequest(res.status_code, res.text)  # 例外のargはすべて右の通り: int(statuscode), str(text)
        elif res.status_code == 401:
            raise InvalidAPIKey(res.status_code, res.text)
        elif res.status_code == 404:
            raise ResourceNotFound(res.status_code, res.text)
        elif res.status_code == 500:
            raise InternalServerError(res.status_code, res.text)
        else:
            raise ResponseNot200(res.status_code, res.text)

    @overload
    def get_document_list(self, date: datetime.datetime, type_: Literal[1]) -> GetDocumentResponse: ...
    @overload
    def get_document_list(self, date: datetime.datetime, type_: Literal[2]) -> GetDocumentResponseWithDocs: ...
    @overload
    def get_document_list(self, date: datetime.datetime) -> GetDocumentResponse: ...

    def get_document_list(self,
                          date: datetime.datetime,
                          type_: Literal[1, 2] = 1) -> Union[GetDocumentResponse, GetDocumentResponseWithDocs]:
        """
        `documents.json`エンドポイントのラッパー
        date: `datetime.datetime`オブジェクト
        type_: 1か2の値、デフォルト値は1
        """
        if isinstance(date, datetime.datetime) and type_ in (1, 2):  # 引数があっているか確認

            params = {
                "date": date.strftime("%Y-%m-%d"),
                "type": type_
            }

            response = self.__request(endpoint="documents.json",
                                      params=params)

            return response.json()

        else:
            raise ValueError()

    def get_document(self,
                     docId: str,
                     type_: Literal[1, 2, 3, 4, 5]) -> bytes:
        """
        `documents/{docId}`エンドポイントのラッパー
        docId: ドキュメントのID
        type_: 1~5の値。それぞれ何に対応するかはAPI仕様書を参考にしてください
        """
        if type_ in (1, 2, 3, 4, 5):

            params = {
                "type": type_
            }

            response = self.__request(endpoint=f"documents/{docId}",
                                      params=params)

            return response.content

        else:
            raise ValueError()
