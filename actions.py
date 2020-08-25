# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import requests
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


class FamousPeopleForm(FormAction):
    def name(self) -> Text:
        return "form_famous_people_drenova"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["famous_person"]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:

        response = requests.get(f"https://hr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={tracker.get_slot('famous_person')}")

        content = json.loads(response.content.decode("utf-8"))
        for key, value in content["query"]["pages"].items():
            if value["title"] == tracker.get_slot('famous_person'):
                dispatcher.utter_message(value["extract"])
                break
        return []
