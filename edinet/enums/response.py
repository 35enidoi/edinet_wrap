from typing import TypedDict, Literal, Union


class GetDocumentResultSet(TypedDict):
    count: int


class GetDocumentParam(TypedDict):
    date: Literal["YYYY-MM-DD"]
    type: str


class GetDocumentMetadata(TypedDict):
    title: str
    parameter: GetDocumentParam
    resultset: GetDocumentResultSet
    processDateTime: Literal["YYYY-MM-DD hh:mm"]
    status: str
    message: str


class GetDocumentDocs(TypedDict):
    seqNumber: int
    docID: str
    edinetCode: Union[None, str]
    secCode: Union[None, str]
    JCN: Union[None, str]
    filerName: Union[None, str]
    fundCode: Union[None, str]
    ordinanceCode: Union[None, str]
    formCode: Union[None, str]
    docTypeCode: Union[None, str]
    periodStart: Union[None, Literal["YYYY-MM-DD"]]
    periodEnd: Union[None, Literal["YYYY-MM-DD"]]
    submitDateTime: Literal["YYYY-MM-DD hh:mm"]
    docDescription: Union[None, str]
    issuerEdinetCode: Union[None, str]
    subjectEdinetCode: Union[None, str]
    subsidiaryEdinetCode: Union[None, str]
    currentReportReason: Union[None, str]
    parentDocID: Union[None, str]
    opeDateTime: Union[None, Literal["YYYY-MM-DD hh:mm"]]
    withdrawalStatus: Literal["0", "1", "2"]
    docInfoEditStatus: Literal["0", "1", "2"]
    disclosureStatus: Literal["0", "1", "2", "3"]
    xbrlFlag: Literal["0", "1"]
    pdfFlag: Literal["0", "1"]
    attachDocFlag: Literal["0", "1"]
    englishDocFlag: Literal["0", "1"]
    csvFlag: Literal["0", "1"]
    legalStatus: Literal["0", "1", "2"]


class GetDocumentResponse(TypedDict):
    metadata: GetDocumentMetadata


class GetDocumentResponseWithDocs(TypedDict):
    metadata: GetDocumentMetadata
    results: list[GetDocumentDocs]
