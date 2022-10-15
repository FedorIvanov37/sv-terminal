from datetime import datetime, timedelta
from PyQt5.Qt import QObject
from common.app.data_models.message import Message
from common.app.core.tools.epay_specification import EpaySpecification
from logging import warning


class Transaction(QObject):
    _spec: EpaySpecification = EpaySpecification()
    _request: Message | None = None
    _response: Message | None = None
    _timer: timedelta = None
    _timer_started: bool = False
    _matched: bool = False
    _trans_id: str = str()
    _utrnno: str | None = str()
    _start_time: datetime = None

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def utrnno(self):
        return self._utrnno

    @utrnno.setter
    def utrnno(self, utrnno):
        self._utrnno = utrnno

    @property
    def spec(self):
        return self._spec

    @property
    def trans_id(self):
        return self._trans_id

    @trans_id.setter
    def trans_id(self, trans_id):
        self._trans_id = trans_id

    @property
    def matched(self):
        return self._matched

    @matched.setter
    def matched(self, matched):
        self._matched = matched

    @property
    def timer_started(self):
        return self._timer_started

    @timer_started.setter
    def timer_started(self, timer_started: bool):
        self._timer_started = timer_started

    @property
    def timer(self):
        return datetime.now() - self.start_time if self._timer_started else self._timer

    @timer.setter
    def timer(self, timer):
        self._timer = timer

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        self._request = request

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self._response = response

    def __init__(self, request=None, trans_id=None):
        QObject.__init__(self)
        self.trans_id = trans_id
        self.put_request(request)

    def match(self, request: Message = None, response: Message = None):
        if self.matched:
            return False

        if request is None:
            request: Message = self.request

        if response is None:
            response: Message = self.response

        if request is None and response is None:
            return False

        resp_type = self.spec.get_resp_mti(request.transaction.message_type_indicator)

        if resp_type != response.transaction.message_type_indicator:
            return False

        for field in self.spec.get_match_fields():
            if request.transaction.fields.get(field) != response.transaction.fields.get(field):
                return False

        self.matched = True

        return self.matched

    def set_request_trans_id(self, path, value):
        # TODO
        try:
            self.request.transaction.fields[path[0]][path[1]] = value
        except KeyError:
            return

    def put_request(self, request: Message):
        if request is None:
            return

        self.request: Message = request

    def set_utrnno(self, message: Message | None = None) -> None:
        if message is None:
            message = self.response

        if self.response is None:
            return

        utrnno_path = self.spec.get_utrnno_path()
        fields = message.transaction.fields.copy()

        for field in utrnno_path:
            fields = fields.get(field)

            if fields is None:
                self.utrnno = ""
                return

        utrnno = fields

        try:
            self.utrnno = utrnno
            self.request.transaction.utrnno = utrnno
            self.response.transaction.utrnno = utrnno

        except AttributeError:
            warning("Cannot set utrnno for transaction")

    def put_response(self, response: Message):
        self.response: Message = response
        self._stop_timer()
        self.matched = self.match()
        self.set_utrnno()

    def start_timer(self):
        self.start_time = datetime.now()
        self.timer_started = True

    def _stop_timer(self):
        self.timer = datetime.now() - self.start_time
        self.timer_started = False
