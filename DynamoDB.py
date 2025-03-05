from datetime import datetime

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.skill_builder import SkillBuilder

import logging
import json
import random
import os
import boto3
from boto3.dynamodb.conditions import Key 

# Establish connection with AWS DynamoDB

role_arn = "arn:aws:iam::054692298551:role/AlexaHostedLambdaRole"
table_name = 'alexa_hosted_table'

sts_client = boto3.client('sts')
assumed_role_object=sts_client.assume_role(RoleArn=role_arn, RoleSessionName='Session1')
credentials=assumed_role_object['Credentials']

dynamodb = boto3.resource('dynamodb',
                  aws_access_key_id=credentials['AccessKeyId'],
                  aws_secret_access_key=credentials['SecretAccessKey'],
                  aws_session_token=credentials['SessionToken'],
                  region_name='us-east-1')

table = dynamodb.Table(table_name)

# Initializing the logger and setting the level to "INFO"
# Read more about it here https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Intent Handlers

# This Handler is called when the skill is invoked by using only the invocation name(Ex. Alexa, open template ten)
class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        skill_name = language_prompts["SKILL_NAME"]
        user_id = handler_input.request_envelope.session.user.user_id
        
        try:
            response = table.get_item(
                Key={
                    'user_id': user_id
                }
            )
            item = response['Item']
            user_name = item['user_name']
            speech_output = random.choice(language_prompts["REPEAT_USER_GREETING"]).format(user_name)
            reprompt = random.choice(language_prompts["REPEAT_USER_GREETING_REPROMPT"])
        
        except:
            speech_output = random.choice(language_prompts["FIRST_TIME_USER"]).format(skill_name)
            reprompt = random.choice(language_prompts["FIRST_TIME_USER_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class MyNameIsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MyNameIsIntent")(handler_input)
    
    def handle(self,handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        user_id = handler_input.request_envelope.session.user.user_id
        user_name = handler_input.request_envelope.request.intent.slots["UserNameSlot"].value
        time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        item_type = 'book'
        item = 'Inner Engineering'
        
        table.put_item(
            Item={
                'user_id': user_id,
                'user_name': user_name,
                'Time_stamp': time_stamp,
                'item_type': item_type,
                'item': item,
                'test_id': '8aa'
            }
        )
        
        speech_output = random.choice(language_prompts["NAME_SAVED"]).format(user_name)
        reprompt = random.choice(language_prompts["NAME_SAVED_REPROMPT"])
        
        return(
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class WhatsMyNameIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("WhatsMyNameIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        user_id = handler_input.request_envelope.session.user.user_id
        
        print("I AM BEFORE TRY!!!!")
        try:
            
            response = table.query(KeyConditionExpression=Key('user_id').eq("amzn1.ask.account.AMAYIQDXPR5KNTFNOL7EEMVQYRN4NBAOIRD6GX62MVOBO4LDGA4IKVPDPL5FJCBIPDADWI4AHS4Q7AQTYORBTSZLL52EFDJELNTFVLUOWQYX32EEZWOLQ2LI4RVSQX4PFHJ3AJ44DGFYAF3NBQRQJ3Z3RIONBT6E7XROL7SOSMNMQSA3Q2SSY35S64HE6BXSJXLGADH2PXJNNGYD4KJ6FXSYRL2UHCOMM5VAYY64HBWQ"))
            #Ranojoy#response = table.query(KeyConditionExpression=Key('user_id').eq("amzn1.ask.account.AMAVWO5O3XIXQH2PQMDVHYV32GVGZQVDQWOQCJN7WE4WSBPMIUYCWYJVIIGW5I2LJVWU6A4DK4ZLW672Z76A64OSROKDFWIMHQPUS5RALC3F2LZPLC53HI5MEO5EBVISBHW7TLV6ZTGNE2AYATXC22TX5MMBN4V7DGFDWJLZUD2EHW4WD3WXCRR6BCKPNHUWTPJGGM2Q5FZN2NS4YBIFTLMBWFYIB6YYP6PLD5ALSBMA"))
            '''response = table.get_item(
                Key={
                    'user_id': user_id,
                    'Time_stamp': "29/06/2023 09:29:18"  #Added by Arman
                }
            )'''
            print("I AM AFTER RESPONSE!!!!")
            print("HERE IS response:::"+ str(response))
            item = response['Items'][1]
            user_name = item['user_name']
            
            speech_output = random.choice(language_prompts["TELL_NAME"]).format(user_name)
            reprompt = random.choice(language_prompts["TELL_NAME_REPROMPT"])
        except Exception as e:
            print("I AM IN EXPEPTION!!!!"+ str(e))
            speech_output = random.choice(language_prompts["NO_NAME"])
            reprompt = random.choice(language_prompts["NO_NAME_REPROMPT"])        
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class WhatsLastItemIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return is_intent_name("LastItemIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        user_id = handler_input.request_envelope.session.user.user_id
        
        print("I AM BEFORE TRY!!!!")
        try:
            
            response = table.query(KeyConditionExpression=Key('user_id').eq("amzn1.ask.account.AMAYIQDXPR5KNTFNOL7EEMVQYRN4NBAOIRD6GX62MVOBO4LDGA4IKVPDPL5FJCBIPDADWI4AHS4Q7AQTYORBTSZLL52EFDJELNTFVLUOWQYX32EEZWOLQ2LI4RVSQX4PFHJ3AJ44DGFYAF3NBQRQJ3Z3RIONBT6E7XROL7SOSMNMQSA3Q2SSY35S64HE6BXSJXLGADH2PXJNNGYD4KJ6FXSYRL2UHCOMM5VAYY64HBWQ"))
            #Ranojoy#response = table.query(KeyConditionExpression=Key('user_id').eq("amzn1.ask.account.AMAVWO5O3XIXQH2PQMDVHYV32GVGZQVDQWOQCJN7WE4WSBPMIUYCWYJVIIGW5I2LJVWU6A4DK4ZLW672Z76A64OSROKDFWIMHQPUS5RALC3F2LZPLC53HI5MEO5EBVISBHW7TLV6ZTGNE2AYATXC22TX5MMBN4V7DGFDWJLZUD2EHW4WD3WXCRR6BCKPNHUWTPJGGM2Q5FZN2NS4YBIFTLMBWFYIB6YYP6PLD5ALSBMA"))
            
            item_count = response['Count']
            print("I AM AFTER RESPONSE!!!!")
            print("HERE IS response:::"+ str(response))
            item = response['Items'][item_count-1]
            user_name = item['user_name']
            
            speech_output = random.choice(language_prompts["TELL_NAME"]).format(user_name)
            reprompt = random.choice(language_prompts["TELL_NAME_REPROMPT"])
        except Exception as e:
            speech_output = random.choice(language_prompts["NO_NAME"])
            reprompt = random.choice(language_prompts["NO_NAME_REPROMPT"])        
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )


class UpdateNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("UpdateNameIntent")(handler_input)
    
    def handle(self,handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        user_id = handler_input.request_envelope.session.user.user_id
        user_name = handler_input.request_envelope.request.intent.slots["NewNameSlot"].value
        
        table.update_item(
            Key={
                'user_id': user_id
            },
            UpdateExpression='SET user_name = :val1',
            ExpressionAttributeValues={
                ':val1': user_name
            }
        )
        
        speech_output = random.choice(language_prompts["NAME_UPDATED"]).format(user_name)
        reprompt = random.choice(language_prompts["NAME_UPDATED_REPROMPT"])
        
        return(
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class DeleteNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DeleteNameIntent")(handler_input)
    
    def handle(self,handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        user_id = handler_input.request_envelope.session.user.user_id
        
        table.delete_item(
            Key={
                'user_id': user_id
            }
        )
        
        speech_output = random.choice(language_prompts["NAME_DELETED"])
        reprompt = random.choice(language_prompts["NAME_DELETED_REPROMPT"])
        
        return(
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["CANCEL_STOP_RESPONSE"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["HELP"])
        reprompt = random.choice(language_prompts["HELP_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# This handler handles utterances that can't be matched to any other intent handler.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["FALLBACK"])
        reprompt = random.choice(language_prompts["FALLBACK_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class SessionEndedRequesthandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with the reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Exception Handlers

# This exception handler handles syntax or routing errors. If you receive an error stating 
# the request handler is not found, you have not implemented a handler for the intent or 
# included it in the skill builder below
class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = language_prompts["ERROR"]
        reprompt = language_prompts["ERROR_REPROMPT"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# Interceptors

# This interceptor logs each request sent from Alexa to our endpoint.
class RequestLogger(AbstractRequestInterceptor):

    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

# This interceptor logs each response our endpoint sends back to Alexa.
class ResponseLogger(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

# This interceptor is used for supporting different languages and locales. It detects the users locale,
# loads the corresponding language prompts and sends them as a request attribute object to the handler functions.
class LocalizationInterceptor(AbstractRequestInterceptor):

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        
        try:
            with open("languages/"+str(locale)+".json") as language_data:
                language_prompts = json.load(language_data)
        except:
            with open("languages/"+ str(locale[:2]) +".json") as language_data:
                language_prompts = json.load(language_data)
        
        handler_input.attributes_manager.request_attributes["_"] = language_prompts


# Skill Builder
# Define a skill builder instance and add all the request handlers,
# exception handlers and interceptors to it.

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MyNameIsIntentHandler())
sb.add_request_handler(WhatsMyNameIntentHandler())
sb.add_request_handler(WhatsLastItemIntentHandler())
sb.add_request_handler(UpdateNameIntentHandler())
sb.add_request_handler(DeleteNameIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequesthandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()
