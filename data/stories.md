## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
  
## famous people drenova
* find_famous_people_drenova
  - utter_find_famous_people_drenova
* famous_people_drenova{"famous_person": "Fran Franković"}
  - form_famous_people_drenova
  - form{"name": "form_famous_people_drenova"}
  - form{"name": null}
  
## slideshow
* start_slideshow
  - utter_slideshow
* next
  - utter_next
* past
  - utter_past
