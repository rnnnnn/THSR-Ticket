import json
from typing import Tuple

from bs4 import BeautifulSoup
from requests.models import Response

from thsr_ticket.configs.web.param_schema import ConfirmTicketModel
from thsr_ticket.model.db import Record
from thsr_ticket.remote.http_request import HTTPRequest

class ConfirmTicketFlow:
    def __init__(self, client: HTTPRequest, train_resp: Response, record: Record = None):
        self.client = client
        self.train_resp = train_resp
        self.record = record

    def run(self, data: dict) -> Tuple[Response, ConfirmTicketModel]:
        # Verify the data.
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary.")
        for key in ["ID_number", "phone_number", "email_address"]:
            if key not in data:
                raise ValueError(f"Key '{key}' not found in data.")

        page = BeautifulSoup(self.train_resp.content, features='html.parser')
        ticket_model = ConfirmTicketModel(
            personal_id=self.set_personal_id(ID_number=data["ID_number"]),
            phone_num=self.set_phone_num(phone_number=data["phone_number"]),
            email=self.set_email_address(email_address=data["email_address"]),
            member_radio=_parse_member_radio(page),
            member_account=_parse_member_account(page, ID_number=data["ID_number"]),
        )

        json_params = ticket_model.json(by_alias=True)
        dict_params = json.loads(json_params)
        resp = self.client.submit_ticket(dict_params)
        return resp, ticket_model

    def set_personal_id(self, ID_number) -> str:
        print(f"Personal number: {ID_number}\r\n")
        if self.record and (personal_id := self.record.personal_id):
            return personal_id
        return ID_number

    def set_phone_num(self, phone_number) -> str:
        print(f"Phone number: {phone_number}\r\n")
        if self.record and self.record.phone:
            return self.record.phone
        return phone_number

    def set_email_address(self, email_address) -> str:
        print(f"Email address: {email_address}\r\n")
        if self.record and self.record.email:
            return self.record.email
        return email_address


def _parse_member_radio(page: BeautifulSoup) -> str:
    candidates = page.find(
        'input',
        attrs={
            'name': 'TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup',
            'id': 'memberSystemRadio1'
        },
    )
    return candidates.attrs['value'] if candidates else ''


def _parse_member_account(page: BeautifulSoup, ID_number) -> str:
    candidates = page.find(
        'input',
        attrs={
            'name': 'TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup:memberShipNumber'
        },
    )
    return ID_number if candidates else ''
