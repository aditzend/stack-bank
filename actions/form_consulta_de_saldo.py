from gc import collect
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import requests
import os


# CMS_URL = os.environ.get('CMS_URL')
# CMS_PORT = os.environ.get('CMS_PORT')
CMS_API_URL = os.environ.get("CMS_API_URL")


class ActionInformarSaldo(Action):
    def name(self) -> Text:
        return "action_informar_saldo"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dni = tracker.get_slot("user_dni")
        if type(dni) is list:
            dni = dni[0]
        r = requests.get(f"{CMS_API_URL}/items/cuentas?filter[dni][_eq]={dni}")
        response = r.json()["data"]
        if response:
            if (
                response[0]["saldo"]
                and response[0]["moneda"]
                and response[0]["titular"]
            ):
                saldo = response[0]["saldo"]
                moneda = response[0]["moneda"]
                titular = response[0]["titular"]

                dispatcher.utter_message(
                    text=(
                        f"La cuenta a nombre de {titular} cuenta con un saldo"
                        f" de {moneda} {saldo} ."
                    )
                )
        else:
            dispatcher.utter_message(
                text=f"No he podido encontrar una cuenta con el número {dni} ."
            )

        return []


# class ValidateFormConsultaDeSaldo(FormValidationAction):

#     def name(self) -> Text:
#         return "validate_form_consulta_de_saldo"

#     def validate_user_dni(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:

#         # r = requests.get(f'http://192.168.43.169:{CMS_PORT}/items/cuentas?filter[dni][_eq]=29984695?fields=dni')
#         r = requests.get(f'{CMS_URL}:{CMS_PORT}/items/cuentas?filter[dni][_eq]={value}')
#         response = r.json()['data']
#         print('\n\n\n')
#         print('Validate DNI')
#         print(response)

#         """Validate DNI"""
#         if response[0] == []:
#             dispatcher.utter_message(response="utter_dni_no_encontrado")
#             return {"user_dni": None}
#         else:

#             # dispatcher.utter_message(text=f'Tu saldo en la cuenta {value} es {saldo}')
#             return {"user_dni": value}

# class SubmitFormConsultaDeSaldo(Action):
#     def name(self) -> Text:
#         return "utter_submit_form_consulta_de_saldo"

#     def run(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,

#     )
