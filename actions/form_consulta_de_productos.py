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


class ActionInformarProductosDisponibles(Action):
    def name(self) -> Text:
        return "action_informar_productos_disponibles"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dni = tracker.get_slot("user_dni")
        if type(dni) is list:
            dni = dni[0]
        r = requests.get(
            f"{CMS_API_URL}/items/productos?filter[dni][_eq]={dni}"
        )
        response = r.json()["data"]
        if response:
            if response[0]:
                producto = response[0]["producto"]
                dispatcher.utter_message(
                    text=f"Encontré un producto disponible. {producto}."
                )

        else:
            dispatcher.utter_message(
                text=(
                    "No he podido encontrar productos disponibles para la"
                    f" cuenta {dni}."
                )
            )

        return []
