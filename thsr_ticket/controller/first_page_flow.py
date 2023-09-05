import io
import json
from PIL import Image
from typing import Tuple
from datetime import datetime
from bs4 import BeautifulSoup
from requests.models import Response

from thsr_ticket.model.db import Record
from thsr_ticket.remote.http_request import HTTPRequest
from thsr_ticket.configs.web.param_schema import BookingModel
from thsr_ticket.configs.web.parse_html_element import BOOKING_PAGE
from thsr_ticket.configs.web.enums import StationMapping, TicketType
from thsr_ticket.configs.common import (
    AVAILABLE_TIME_TABLE,
)
from extra import image_process


class FirstPageFlow:
    def __init__(self, client: HTTPRequest, record: Record = None) -> None:
        self.client = client
        self.record = record

    def run(self, data) -> Tuple[Response, BookingModel]:
        # First page. Booking options
        book_page = self.client.request_booking_page().content
        img_resp = self.client.request_security_code_img(book_page).content
        page = BeautifulSoup(book_page, features='html.parser')

        book_model = BookingModel(
            start_station=self.select_station('Departure', default_value=data["start_station"]),
            dest_station=self.select_station('Arrival', default_value=data["dest_station"]),
            outbound_date=self.select_date('Date', default_value=data["date"]),
            outbound_time=self.select_time('Time', default_value=data["time"]),
            adult_ticket_num=self.select_ticket_num(TicketType.ADULT),
            seat_prefer=_parse_seat_prefer_value(page),
            types_of_trip=_parse_types_of_trip_value(page),
            search_by=_parse_search_by(page),
            security_code=_input_security_code(img_resp),
        )
        json_params = book_model.model_dump_json(by_alias=True)
        dict_params = json.loads(json_params)
        resp = self.client.submit_booking_form(dict_params)
        return resp, book_model

    def select_station(self, travel_type: str, default_value) -> int:
        if (
            self.record
            and (
                station := {
                    'Departure': self.record.start_station,
                    'Arrival': self.record.dest_station,
                }.get(travel_type)
            )
        ):
            return station

        print(f'Select {travel_type} Station: {StationMapping(int(default_value)).name} Station \r\n')
        return default_value

    def select_date(self, date_type: str, default_value) -> str:
        print(f'Select {date_type}: {default_value}\r\n')
        return default_value

    def select_time(self, time_type: str, default_value: str) -> str:
        if self.record and (
            time_str := {
                'Departure': self.record.outbound_time,
                'Return': None,
            }.get(time_type)
        ):
            return time_str

        time_str = AVAILABLE_TIME_TABLE[int(default_value) - 1]
        if time_str.endswith('N'):
            time_str = time_str.replace('N', 'PM')
        elif time_str.endswith('A'):
            time_str = time_str.replace('A', 'AM')
        else:
            time_str = time_str.replace('P', 'PM')
        selected_time = datetime.strptime(time_str, '%I%M%p').time()
        formatted_time = selected_time.strftime('%I%M%p').lstrip('0')  # 12-hour format without leading 0
        print(f"Selected {time_type}: {formatted_time}\r\n")
        return AVAILABLE_TIME_TABLE[int(default_value) - 1]

    def select_ticket_num(self, ticket_type: TicketType, default_ticket_num: int = 1) -> str:
        if self.record and (
            ticket_num_str := {
                TicketType.ADULT: self.record.adult_num,
                TicketType.CHILD: None,
                TicketType.DISABELD: None,
                TicketType.ELDER: None,
                TicketType.COLLEGE: None,
            }.get(ticket_type)
        ):
            return ticket_num_str

        ticket_type_name = {
            TicketType.ADULT: 'Adult',
            TicketType.CHILD: 'Child',
            TicketType.DISABELD: 'Disability',
            TicketType.ELDER: 'Elderly',
            TicketType.COLLEGE: 'College',
        }.get(ticket_type)

        print(f'Select {ticket_type_name} Ticket Number: {default_ticket_num}\r\n')
        return f'{default_ticket_num}{ticket_type.value}'


def _parse_option_value(page: BeautifulSoup, option: str) -> str:
    options = page.find(**BOOKING_PAGE[option])
    selected_option = options.find(selected='selected')
    return selected_option.attrs['value']

def _parse_seat_prefer_value(page: BeautifulSoup) -> str:
    return _parse_option_value(page, 'seat_prefer_radio')

def _parse_types_of_trip_value(page: BeautifulSoup) -> int:
    return int(_parse_option_value(page, 'types_of_trip'))

def _parse_search_by(page: BeautifulSoup) -> str:
    tag = page.find('input', {'name': 'bookingMethod', 'checked': True})
    return tag.attrs['value']

def _input_security_code(img_resp: bytes) -> str:
    image = Image.open(io.BytesIO(img_resp))
    result = image_process.verify_code(image)
    print(f'Verification Code: {result}\r\n')
    return result
