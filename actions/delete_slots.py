from gc import collect
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction


class ActionDeleteSlots(Action):
    def name(self) -> Text:
        return "action_delete_slots"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        #dni = tracker.get_slot("user_dni")
        dispatcher.utter_message(text=f'Ok, pero qué desea hacer?')

        
        return []
    