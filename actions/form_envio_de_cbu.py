from gc import collect
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import requests
import os
import sec

# CMS_URL = os.environ.get('CMS_URL')
# CMS_PORT = os.environ.get('CMS_PORT')
CMS_API_URL = os.environ.get("CMS_API_URL")
EMAIL_URL = sec.load("email_url")
EMAIL_API_KEY = sec.load("email_api_key")


class ActionEnviarCbu(Action):
    def name(self) -> Text:
        return "action_enviar_cbu"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        name = tracker.get_slot("user_name")
        email = tracker.get_slot("user_email")
        dni = tracker.get_slot("user_dni")
        if type(dni) is list:
            dni = dni[0]

        r = requests.get(f"{CMS_API_URL}/items/cuentas?filter[dni][_eq]={dni}")
        response = r.json()["data"]
        cbu = response[0]["cbu"]
        print("\n\n\n")
        print("Enviar CBU por mail")
        print(response)
        text = f"Su numero de CBU es {cbu}"
        body = {
            "from": "Aconcagua Bank <aconcagua_bank@sara.ar>",
            "to": email,
            "subject": "Comprobante de CBU",
            "text": text,
        }
        emailJob = requests.post(
            "{EMAIL_URL}", auth=("api", "{EMAIL_API_KEY}"), data=body
        )
        print("\n\n\n")

        print(emailJob.json())

        dispatcher.utter_message(
            text=f"Perfecto, le hemos enviado su CBU al correo  {email}."
        )
        return []


class ValidateFormEnvioDeCbu(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_envio_de_cbu"

    def validate_user_dni(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        r = requests.get(
            f"{CMS_API_URL}/items/cuentas?filter[dni][_eq]={value}"
        )
        response = r.json()["data"]
        print("\n\n\n")
        print("Validate DNI")
        print(response)

        """Validate DNI"""
        if response[0] == []:
            dispatcher.utter_message(response="utter_dni_no_encontrado")
            return {"user_dni": None}
        else:

            # dispatcher.utter_message(text=f'Tu saldo en la cuenta {value} es {saldo}')
            return {"user_dni": value}


# class SubmitFormConsultaDeSaldo(Action):
#     def name(self) -> Text:
#         return "utter_submit_form_consulta_de_saldo"

#     def run(
#         self,
#         value: Text,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,

#     )
