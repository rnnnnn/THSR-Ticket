import re
from typing import Mapping, Any
from jsonschema import validate

from thsr_ticket.model.web.abstract_params import AbstractParams
from thsr_ticket.configs.web.param_schema import CONFIRM_TICKET_SHEMA


class ConfirmTicket(AbstractParams):
    def __init__(self) -> None:
        # User input
        self._personal_id: str = None
        self._phone: str = ""
        self._email: str = ""

        self.id_input_radio: int = 0
        self.member_radio: str = None
        self.member_account: str = None

    def get_params(self, val: bool = True) -> Mapping[str, Any]:
        params = {
            "BookingS3FormSP:hf:0": "",
            "diffOver": 1,
            "idInputRadio": self.id_input_radio,
            "dummyId": self.personal_id,
            "dummyPhone": self.phone,
            "email": self.email,
            "agree": "on",
            "isGoBackM": "",
            "backHome": "",
            "TgoError": "1",
            # "TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup": self.member_radio,
            # "TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup:memberShipNumber": self.member_account,
        }

        if self.member_radio is not None:
            params["TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup"] = self.member_radio
        if self.member_account is not None:
            params["TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup:memberShipNumber"] = self.member_account


        if val:
            validate(params, schema=CONFIRM_TICKET_SHEMA)
        return params

    @property
    def personal_id(self) -> str:
        return self._personal_id

    @personal_id.setter
    def personal_id(self, value: str) -> None:
        if len(value) != 10:
            raise ValueError("Wrong length of R.O.C. ID. Should be 10, received {}".format(len(value)))
        self._personal_id = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        if len(value) != 0 and len(value) != 10:
            raise ValueError("Wrong length of phone number. Should be 10, received {}".format(len(value)))
        if len(value) != 0 and not value.startswith("09"):
            raise ValueError("Wrong prefix with the phone number: {}".format(value))
        self._phone = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, value):
            raise ValueError("Invalid email")
        self._emaile = value

