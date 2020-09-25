## entry path
* greet
  - utter_greet
  - action_show_content
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
  
## show content
* show_content
  - action_show_content
  
## slideshow
* start_slideshow
  - action_start_slideshow
* next
  - utter_next
* past
  - utter_past
  
## video
* start_video
  - action_start_video
* play
  - utter_play
* stop
  - utter_stop
* pause
  - utter_pause
  
## simple term information
* term_information
  - action_term_information
