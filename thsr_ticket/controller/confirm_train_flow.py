import json
from datetime import datetime, timedelta
from typing import List, Tuple

from requests.models import Response

from thsr_ticket.remote.http_request import HTTPRequest
from thsr_ticket.configs.web.param_schema import Train, ConfirmTrainModel
from thsr_ticket.view_model.avail_trains import AvailTrains
from thsr_ticket.configs.common import AVAILABLE_TIME_TABLE

class ConfirmTrainFlow:
    def __init__(self, client: HTTPRequest, book_resp: Response):
        self.client = client
        self.book_resp = book_resp

    def run(self, data) -> Tuple[Response, ConfirmTrainModel]:
        trains = AvailTrains().parse(self.book_resp.content)
        if not trains:
            raise ValueError('No available trains in the response!')

        confirm_model = ConfirmTrainModel(selected_train=self.select_available_trains(trains, data))
        json_params = confirm_model.model_dump_json(by_alias=True)
        dict_params = json.loads(json_params)
        resp = self.client.submit_train(dict_params)
        return resp, confirm_model

    def select_available_trains(self, trains: List[Train], data):
        boarding_time = int(data["time"])
        start_boarding_time_str = AVAILABLE_TIME_TABLE[boarding_time-1]
        start_boarding_time = convert_to_24hr(start_boarding_time_str)
        end_boarding_time = start_boarding_time + timedelta(hours=1)

        for train in trains:
            train_depart_time = datetime.strptime(train.depart, "%H:%M").time()
            if start_boarding_time.time() <= train_depart_time <= end_boarding_time.time():
                print(f'Selected train: {train.depart}~{train.arrive}\r\n')
                return train.form_value

        raise ValueError('No available trains during the desired boarding time.')

def convert_to_24hr(time_str):
    period = time_str[-1]
    time_str = time_str[:-1]

    if len(time_str) <= 3:
        if time_str[0] == '1':
            hour = int(time_str[:2])
            minute = int(time_str[2:]) if time_str[2:] else 0
        else:
            hour = int(time_str[:1])
            minute = int(time_str[1:]) if time_str[1:] else 0
    else:
        hour, minute = int(time_str[:-2]), int(time_str[-2:])

    if period == "P" and hour != 12:
        hour += 12
    elif period == "A" and hour == 12:
        hour = 0
    elif period == "N":
        hour = 12

    return datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M")

