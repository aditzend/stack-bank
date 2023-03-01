from gc import collect
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import requests
import json

class ActionCargarSaldo(Action):
    def name(self) -> Text:
        return "action_cargar_saldo"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dni = tracker.get_slot("user_dni")
        if type(dni) is list:
            dni = dni[0]
        
        monto = tracker.get_slot("amount_of_money")
        if type(monto) is list:
            monto = monto[0]
        moneda = tracker.get_slot("currency")
        if type(moneda) is list:
            moneda = moneda[0]
       

            
        wordCentavos = tracker.get_slot("centavos") or ""
        if type(wordCentavos) is list:
            wordCentavos = wordCentavos[0]
        
        if len(wordCentavos) > 0 :
            monto = float(monto) * 0.01
        
        dispatcher.utter_message(text=f'He procesado {moneda} {monto} en la cuenta {dni}.')
        # r = requests.get(f'{CMS_URL}:{CMS_PORT}/items/cuentas?filter[dni][_eq]={dni}')
        # response = r.json()['data']
        # if response:
        #     if response[0]:
        #         id = response[0]['id']
        #         saldo_anterior = response[0]['saldo']
        #         #saldo_nuevo = saldo_anterior + saldo
        #         saldo_nuevo = 42
        #         p = requests.patch(f'{CMS_URL}:{CMS_PORT}/items/cuentas/1', data={"saldo": f'{saldo_nuevo}'})
        #         patch = p.json()['data']
                
        #         try:
        #             saldo_actualizado = patch[0]['saldo']
        #             dispatcher.utter_message(text=f'He cargado {moneda} {saldo_actualizado} en la cuenta {dni}.')
        #         except:
        #             dispatcher.utter_message(text=f'No he podido cargar saldo para la cuenta {dni}.')
        # else:
        #     dispatcher.utter_message(text=f'No he podido encontrar la cuenta {dni}.')

       
        return []


