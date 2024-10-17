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
        Edinet APIのラッパー

        Parameters
        ----------
        token: str
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
    def get_document_list(self, date: datetime.datetime, withdocs: False) -> GetDocumentResponse: ...
    @overload
    def get_document_list(self, date: datetime.datetime, withdocs: True) -> GetDocumentResponseWithDocs: ...
    @overload
    def get_document_list(self, date: datetime.datetime) -> GetDocumentResponse: ...

    def get_document_list(self,
                          date: datetime.datetime,
                          withdocs: bool = False) -> Union[GetDocumentResponse, GetDocumentResponseWithDocs]:
        """
        `documents.json`エンドポイントのラッパー

        Parameters
        ----------
        date: datetime.datetime
            `datetime.datetime`オブジェクト、年月日の指定。
        withdocs: :obj:`bool`, default False
            提出書類一覧を含めるか、デフォルトは含めない。
        """
        if isinstance(date, datetime.datetime) and isinstance(withdocs, bool):  # 引数があっているか確認

            params = {
                "date": date.strftime("%Y-%m-%d"),
                "type": (withdocs + 1)  # boolはintのサブクラス
            }

            response = self.__request(endpoint="documents.json",
                                      params=params)

            return response.json()

        else:
            raise ValueError()

    def get_document(self,
                     docId: str,
                     type: Literal[1, 2, 3, 4, 5]) -> bytes:
        """
        ドキュメントの取得

        Parameters
        ----------
        docId: str
            書類管理番号
        type: Literal[1, 2, 3, 4, 5]
            - 1: 提出本文書及び監査報告書、XBRLを取得
            - 2: PDFを取得
            - 3: 代替書面・添付文書を取得
            - 4: 英文ファイルを取得
            - 5: CSVを取得
        """
        if type in (1, 2, 3, 4, 5):

            params = {
                "type": type
            }

            response = self.__request(endpoint=f"documents/{docId}",
                                      params=params)

            return response.content

        else:
            raise ValueError()
