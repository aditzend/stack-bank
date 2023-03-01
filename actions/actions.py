from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher

class ActionHi(Action):
    def name(self) -> Text:
        return "action_say_hi"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        dispatcher.utter_message(text = "hola desde action")

        return []