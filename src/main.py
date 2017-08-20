"""
Simple Python Lambda function informing the user if their birthday is contained within the first 
million digits of pi, or if not.
Intents supported:

"""

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(card_title, card_content, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': card_content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Your functions to implement your intents ------------------

### From working on the Good Actor skill, the api call needs to be in the callable function itself to work correctly.

import requests

r = requests.get('https://raw.githubusercontent.com/ehmatthes/pcc/master/chapter_10/pi_million_digits.txt')

pi_string = r.text

for rs in r:
    pi_string += rs.strip()
    
print(pi_string[:32] + "...")
print(len(pi_string))


def birthday_pi(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = True
    
    
    card_output = ""
    speech_output = "<speak>abcde</speak>"

    return build_response(session_attributes, build_speechlet_response
                          ("", card_output, speech_output, reprompt_text, should_end_session))


def stop(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = True
    
    card_output = "Have a nice day! Enjoy all the things you can do with Pi."
    speech_output = "<speak>Thank you for asking Birthday Pi Pi Pi Pig. Have a nice day!</speak>"

    return build_response(session_attributes, build_speechlet_response
                          ("Session Ended", card_output, speech_output, reprompt_text, should_end_session))
                          

#def open_it(intent, session):
#    session_attributes = {}
#    reprompt_text = None
#    speech_output = ""
#    should_end_session = False
    
#    card_output = "Welcome to the Amazon Alexa Skill, Richmond Dog Info!"
#    speech_output = "<speak>Welcome to the Richmond Dog Info Amazon Alexa skill. I can provide you with names of dog parks, places to take your dog swimming, dog-friendly breweries, festivals and events. or good trails to hike with your pooch. And a dog park we recommend. This skill can also provide answers on why dogs might bury bones, eat grass. And how to remove a dog tick, or how to handle massive shedding.</speak>"

#    return build_response(session_attributes, build_speechlet_response
#                          ("Richmond Dog Info", card_output, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for checking the Birthday Pi skill."
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Primary Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    logger.info("on_session_started requestId=" + session_started_request['requestId'] +
                ", sessionId=" + session['sessionId'])
                

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    logger.info("on_launch requestId=" + launch_request['requestId'] +
                ", sessionId=" + session['sessionId'])
    
    # Dispatch to skill's launch
    return build_response({},build_speechlet_response(
        "Birthday Pi", "Welcome to the Amazon Alexa skill, Birthday Pi. Tell me your birthday.", "<speak>Welcome to the Amazon Alexa skill, Birthday Pi. Tell me your birthday. And I will tell you if your birthday appears in the first million digits of pi or if it doesn't.</speak>","",False))


def get_help(intent, session):
    """ Called when the user asks for help """
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = False
    
    card_output = "Here are some things you can ask or tell Richmond Dog Info: What dog parks are in Richmond? Where can I take my dog to swim? What pool can my dog go to? What are good trails for my dog? What dog park do you recommend? Why does my dog eat grass? Why does my dog bury bones? How do you handle shedding? My dog has a tick."
    speech_output = "<speak>Here are some topics you can ask Richmond Dog Info. What dog parks are in Richmond? What do you recommend? Which parts of the river can my dog swim? Where can I take my dog hiking or running? Tell me dog-friendly breweries, events, or festivals. Does your dog have a tick? Ask me how to remove one. Why does my dog eat grass? Why does my dog bury bones. How can I handle my dog's shedding. I also hide an easter egg. <break time=\"1s\"/> I also try mimicking a dog. Just ask me to make a dog noise.</speak>"

    return build_response(session_attributes, build_speechlet_response
                          ("Things to Ask", card_output, speech_output, reprompt_text, should_end_session))


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to skill's intent handlers

    if intent_name == "DogParks":
        return dog_parks(intent, session)
        
    elif intent_name == "Stop":
        return stop(intent, session)
    elif intent_name == "Open":
        return open_it(intent, session)
    elif intent_name == "GetHelp":
        return get_help(intent, session)
#    elif intent_name == "AMAZON.HelpIntent":
#        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    logger.info("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    else:
        return on_session_ended(event['request'], event['session'])
