#!/usr/bin/env python3

import boto3,json,os,urllib3

def lambda_handler(event, context):
  ########################################### Global Variables #####################################################
  BASE_URL = "https://owner-api.teslamotors.com/api/1/vehicles/"
  EVENT_BODY = json.loads(event["body"])
  EVENT_HEADERS = event["headers"]
  TOKEN = EVENT_BODY["TOKEN"]
  VEHICLE_ID = EVENT_BODY["VEHICLE_ID"]
  INPUT_CMD = EVENT_BODY["INPUT_CMD"]
  PARAMETER_1 = EVENT_BODY["PARAMETER_1"]
  PARAMETER_2 = EVENT_BODY["PARAMETER_2"]
  SNS_CLIENT = boto3.client('sns')
  TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

  # If X-Forwarded-For exists then set CLIENT_IP_ADDRESS accordingly
  if "X-Forwarded-For" in EVENT_HEADERS:
    CLIENT_IP_ADDRESS = EVENT_HEADERS["X-Forwarded-For"]
  else:
    CLIENT_IP_ADDRESS = "127.0.0.1"
  ##################################################################################################################
  
  # Function that retrieves the vehicle's status and returns it 
  def GetVehicleState(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'GET',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      VEHICLE_DATA = json.loads(HTTP_REQUEST.data.decode('utf-8'))
      VEHICLE_STATE = VEHICLE_DATA["response"]["state"]

      return(VEHICLE_STATE)

  if INPUT_CMD == "test_command":
    INITIAL_VEHICLE_STATE = "testing"
  else:
    # Capture the INITIAL_VEHICLE_STATE to verify that the vehicle is awake
    INITIAL_VEHICLE_STATE = GetVehicleState(BASE_URL, VEHICLE_ID)

  if INITIAL_VEHICLE_STATE is not None:
    MESSAGE_BODY = {
      "TOKEN": TOKEN,
      "BASE_URL": BASE_URL,
      "VEHICLE_ID": VEHICLE_ID,
      "INPUT_CMD": INPUT_CMD,
      "PARAMETER_1": PARAMETER_1,
      "PARAMETER_2": PARAMETER_2,
      "INITIAL_VEHICLE_STATE": INITIAL_VEHICLE_STATE,
      "CLIENT_IP_ADDRESS": CLIENT_IP_ADDRESS
    }

    MESSAGE_BODY_STR = json.dumps(MESSAGE_BODY)
    MESSAGE_BODY_STR_ENC = MESSAGE_BODY_STR.encode('utf-8')

    # When you publish a message, the client returns a future.
    SNS_RESPONSE = SNS_CLIENT.publish(
        TopicArn=TOPIC_ARN,
        Message=MESSAGE_BODY_STR,
    )
    MESSAGE_ID = SNS_RESPONSE["MessageId"]

    print("Queueing the " + INPUT_CMD + " command for vehicle ID #" + VEHICLE_ID + " on behalf of " + CLIENT_IP_ADDRESS)

    RETURN_DATA = {
      "statusCode": 200,
      "BASE_URL": BASE_URL,
      "VEHICLE_ID": VEHICLE_ID,
      "INPUT_CMD": INPUT_CMD,
      "PARAMETER_1": PARAMETER_1,
      "PARAMETER_2": PARAMETER_2,
      "INITIAL_VEHICLE_STATE": INITIAL_VEHICLE_STATE
    }

    RETURN_DATA_STR = json.dumps(RETURN_DATA)
  else:
    print("ERROR: Exiting as communication with Tesla's APIs failed for vehicle ID #" + VEHICLE_ID + " on behalf of " + CLIENT_IP_ADDRESS)
    RETURN_DATA = {
      "statusCode": 400,
      "BASE_URL": BASE_URL,
      "VEHICLE_ID": VEHICLE_ID,
      "INPUT_CMD": INPUT_CMD,
      "PARAMETER_1": PARAMETER_1,
      "PARAMETER_2": PARAMETER_2,
      "INITIAL_VEHICLE_STATE": INITIAL_VEHICLE_STATE
    }

    RETURN_DATA_STR = json.dumps(RETURN_DATA)

  return {
      'headers': {'Content-Type': 'application/json'},
      'body': RETURN_DATA_STR
  }
