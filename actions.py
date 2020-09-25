# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import enum
import requests
import json
import sqlite3
from fuzzywuzzy import process
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


class ActionShowContent(Action):

    def name(self) -> Text:
        return "action_show_content"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = sqlite3.connect('./chai.db')
        c = conn.cursor()
        c.execute('SELECT * FROM terms')
        terms = c.fetchall()
        c.execute('SELECT * FROM content')
        content = c.fetchall()
        if len(terms) and len(content):
            dispatcher.utter_message(attachment={
                "terms": terms,
                "content": content,
                "type": "content",
                "text": "Sadržaj prikazan sa lijeve strane."})
        conn.close()
        return []


class ActionStartSlideshow(Action):

    def name(self) -> Text:
        return "action_start_slideshow"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["search_terms"]

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("search_terms") is not None:
            data = extract_content_by_search_term(
                QueryDefinitions.SEARCH_TERM_AND_TYPE,
                tracker.get_slot("search_terms"), ("presentation",))

            if len(data):
                dispatcher.utter_message(attachment=data[0])
            else:
                dispatcher.utter_message(("Žao mi je, ali nisam uspio pronaći"
                                          f" prezentaciju pod pojmom {tracker.get_slot('search_terms')}."))
        else:
            dispatcher.utter_message(("Žao mi je, ali nisam uspio pronaći"
                                      " prezentaciju pod traženim pojmom."))

        return []


class ActionDisplayTermInformation(Action):
    def name(self) -> Text:
        return "action_term_information"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["search_terms"]

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("search_terms") is not None:
            data = extract_content_by_search_term(
                QueryDefinitions.SEARCH_TERM,
                tracker.get_slot("search_terms"))

            if len(data):
                dispatcher.utter_message(attachment=data[0])
            else:
                dispatcher.utter_message(("Žao mi je, ali nisam uspio pronaći"
                                          f" informaciju za {tracker.get_slot('search_terms')}."))
        else:
            dispatcher.utter_message(("Žao mi je, ali nisam uspio pronaći"
                                      " informaciju za traženi pojam."))

        return []


class ActionStartVideo(Action):

    def name(self) -> Text:
        return "action_start_video"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["search_terms"]

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("search_terms") is not None:
            data = extract_content_by_search_term(
                QueryDefinitions.SEARCH_TERM_AND_TYPE,
                tracker.get_slot("search_terms"), ("video",))

            if len(data):
                dispatcher.utter_message(attachment=data[0])
            else:
                dispatcher.utter_message(("Žao mi je, ali nisam uspio pronaći "
                                          f"video pod pojmom "
                                          f"{tracker.get_slot('search_terms')}."))
        else:
            dispatcher.utter_message(("Žao mi je, ali nisam uspio pronaći"
                                      " video pod traženim pojmom."))

        return []


def extract_content_by_search_term(query, search_term, arguments=()):
    data = []
    conn = sqlite3.connect('./chai.db')
    c = conn.cursor()
    c.execute('SELECT * FROM terms')
    terms = c.fetchall()
    term_id = fuzzy_match_terms(search_term, terms)
    if term_id is not None:
        arguments = (term_id, *arguments)
        c.execute(query.value, arguments)
        content = c.fetchall()
        data = unpack_rows(c.description, content)
    conn.close()
    return data


def unpack_rows(columns, content):
    columns = tuple([col[0] for col in columns])
    data = list(zip(columns, c) for c in content)
    final_content = []
    for d in data:
        final_content.append(dict(d))
    return final_content


def fuzzy_match_terms(slot_value, terms):
    terms_dict = {term[1]: term[0] for term in terms}
    highest = process.extractOne(slot_value, terms_dict.keys())
    if highest[1] > 50:
        return terms_dict[highest[0]]
    else:
        return None


class QueryDefinitions(enum.Enum):
    SEARCH_TERM_AND_TYPE = ('SELECT c.* FROM term_content tc '
                            'INNER JOIN content c ON c.id = tc.content_id '
                            'WHERE tc.term_id = ? AND c.type = ?')

    SEARCH_TERM = ('SELECT c.* FROM term_content tc '
                   'INNER JOIN content c ON c.id = tc.content_id '
                   'WHERE tc.term_id = ?')

    GET_ALL_TERMS = 'SELECT * FROM terms'


