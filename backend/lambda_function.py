#!/usr/bin/env python3
import json,urllib3,time

def lambda_handler(event, context):
  # Decode pub/sub message body and convert from string back to JSON object
  MESSAGE_BODY_STR = event['Records'][0]['Sns']['Message']
  MESSAGE_BODY = json.loads(MESSAGE_BODY_STR) 

  ########################################### Global Variables #####################################################
  BASE_URL = "https://owner-api.teslamotors.com/api/1/vehicles/"
  TOKEN = MESSAGE_BODY["TOKEN"]
  VEHICLE_ID = MESSAGE_BODY["VEHICLE_ID"]
  INPUT_CMD = MESSAGE_BODY["INPUT_CMD"]
  PARAMETER_1 = MESSAGE_BODY["PARAMETER_1"]
  PARAMETER_2 = MESSAGE_BODY["PARAMETER_2"]
  CLIENT_IP_ADDRESS = MESSAGE_BODY["CLIENT_IP_ADDRESS"]
  INITIAL_VEHICLE_STATE = MESSAGE_BODY["INITIAL_VEHICLE_STATE"]
  ##################################################################################################################

  ############################################### FUNCTIONS ########################################################
  # Function that is used for stack testing
  def TestFunction(BASE_URL, VEHICLE_ID):
    # Variables
    TESTVAR = "TESTVAR_VALUE"

    return(TESTVAR)

  # Function that retrieves the vehicle's data and returns it 
  def GetVehicleData(BASE_URL, VEHICLE_ID):
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
    VEHICLE_DATA = json.loads(HTTP_REQUEST.data.decode('utf-8'))

    return(VEHICLE_DATA)

  # Function that retrieves the vehicle's drive data and returns it 
  def GetVehicleDriveData(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + '/data_request/drive_state'
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'GET',
      URL,
      headers=HEADERS
    )
    VEHICLE_DATA = json.loads(HTTP_REQUEST.data.decode('utf-8'))

    return(VEHICLE_DATA)

  # Function that retrieves the vehicle's status and returns it 
  def GetVehicleState(BASE_URL, VEHICLE_ID):
    VEHICLE_DATA = GetVehicleData(BASE_URL, VEHICLE_ID)
    VEHICLE_STATE = VEHICLE_DATA["response"]["state"]

    return(VEHICLE_STATE)

  # Function that retrieves the vehicle's GPS location and returns it
  def GetVehicleLocation(BASE_URL, VEHICLE_ID):
    # Variables
    VEHICLE_DATA = GetVehicleDriveData(BASE_URL, VEHICLE_ID)
    VEHICLE_LATITUDE = VEHICLE_DATA["response"]["latitude"]
    VEHICLE_LONGITUDE = VEHICLE_DATA["response"]["longitude"]

    return[VEHICLE_LATITUDE, VEHICLE_LONGITUDE]

  # Function that determines the driver's seat position
  def GetDriverSeatPosition(BASE_URL, VEHICLE_ID):
    # Variables
    VEHICLE_DATA = GetVehicleData(BASE_URL, VEHICLE_ID)
    VEHICLE_OPTION_CODES = VEHICLE_DATA["response"]["option_codes"]

    if "DRLH" in VEHICLE_OPTION_CODES:
      DRIVER_SEAT_POSITION = 0
    else:
      DRIVER_SEAT_POSITION = 1

    return(DRIVER_SEAT_POSITION)

  # Function that determines the front passenger's seat position
  def GetFrontPassengerSeatPosition(BASE_URL, VEHICLE_ID):
    # Variables
    DRIVER_SEAT_POSITION = GetDriverSeatPosition(BASE_URL, VEHICLE_ID)
    
    if DRIVER_SEAT_POSITION == 0:
      FRONT_PASSENGER_SEAT_POSITION = 1
    else:
      FRONT_PASSENGER_SEAT_POSITION = 0

    return(FRONT_PASSENGER_SEAT_POSITION)

  # Function that wakes the vehicle
  def WakeVehicle(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/wake_up"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status
    
    # Only for debug
    # HTTP_REQUEST = URL + HEADERS
    # HTTP_REQUEST_STATUS_CODE = 200

    if HTTP_REQUEST_STATUS_CODE == 200:
      # Waiting for the vehicle to wake up before returning
      while GetVehicleState(BASE_URL, VEHICLE_ID) != "online":
        # Variables
        COUNTER = 0

        if COUNTER > 20:
          print("ERROR: Exiting as the vehicle is not waking up...")
          exit(1)
        else:
          # Sleep for 1 second and increment COUNTER
          time.sleep(1)
          COUNTER = COUNTER + 1
    else:
      print("ERROR: The vehicle failed to receive the wake up command")

  # Function that locks the vehicle's doors
  def LockDoors(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/door_lock"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's doors are locked")
    else:
      print("ERROR: The vehicle failed to receive the door lock command")

  # Function that unlocks the vehicle's doors
  def UnlockDoors(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/door_unlock"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's doors are unlocked")
    else:
      print("ERROR: The vehicle failed to receive the door unlock command")

  # Function that activates the vehicle's horn
  def HonkHorn(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/honk_horn"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's horn has been activated")
    else:
      print("ERROR: The vehicle failed to receive the honk horn command")

  # Function that flashes the vehicle's headlights
  def FlashLights(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/flash_lights"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's lights have been flashed")
    else:
      print("ERROR: The vehicle failed to receive the flash lights command")

  # Function that activates the vehicle's Climate Control system
  def StartClimateControl(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/auto_conditioning_start"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's Climate Control system has been activated")
    else:
      print("ERROR: The vehicle failed to receive the start Climate Control system command")

  # Function that deactivates the vehicle's Climate Control system
  def StopClimateControl(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/auto_conditioning_stop"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's Climate Control system has been deactivated")
    else:
      print("ERROR: The vehicle failed to receive the stop Climate Control system command")

  # Function that sets the vehicle's temperature in Celsius
  def SetTemps(BASE_URL, VEHICLE_ID, VEHICLE_TEMP):
    # Variables
    DATA = {
      'driver_temp': VEHICLE_TEMP,
      'passenger_temp': VEHICLE_TEMP
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_temps"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's Climate Control system temperature has been set to " + VEHICLE_TEMP + " degrees Celsius")
    else:
      print("ERROR: The vehicle failed to receive the set Climate Control system temperature command")

  # Function that activates the vehicle's defrost mode
  def StartDefrost(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'on': 1
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_preconditioning_max"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's defrost mode has been activated")
    else:
      print("ERROR: The vehicle failed to receive the start defrost mode command")

  # Function that deactivates the vehicle's defrost mode
  def StopDefrost(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'on': 0
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_preconditioning_max"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's defrost mode has been deactivated")
    else:
      print("ERROR: The vehicle failed to receive the stop defrost mode command")

  # Function that sets the selected seat heater to the defined level
  def SetSeatHeater(BASE_URL, VEHICLE_ID, SEAT_HEATER_POSITION, SEAT_HEATER_LEVEL):
    DATA = {
      'heater': SEAT_HEATER_POSITION,
      'level': SEAT_HEATER_LEVEL
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/remote_seat_heater_request"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status
    
    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's " + str(SEAT_HEATER_POSITION) + " seat heater has been set to " + str(SEAT_HEATER_LEVEL))
    else:
      print("ERROR: The vehicle failed to receive the set seat heater command")

  # Function that activates the driver's seat heater
  def StartDriverSeatHeater(BASE_URL, VEHICLE_ID):
    # Variables
    DRIVER_SEAT_POSITION = GetDriverSeatPosition(BASE_URL, VEHICLE_ID)
    SEAT_HEATER_LEVEL = 3

    SetSeatHeater(BASE_URL, VEHICLE_ID, DRIVER_SEAT_POSITION, SEAT_HEATER_LEVEL)

  # Function that activates the front passenger's seat heater
  def StartFrontPassengerSeatHeater(BASE_URL, VEHICLE_ID):
    # Variables
    DRIVER_SEAT_POSITION = GetDriverSeatPosition(BASE_URL, VEHICLE_ID)
    SEAT_HEATER_LEVEL = 3
    if DRIVER_SEAT_POSITION == 0:
      FRONT_PASSENGER_SEAT_POSITION = 1
    else:
      FRONT_PASSENGER_SEAT_POSITION = 0
    
    SetSeatHeater(BASE_URL, VEHICLE_ID, FRONT_PASSENGER_SEAT_POSITION, SEAT_HEATER_LEVEL)

  # Function that deactivates the driver's seat heater
  def StopDriverSeatHeater(BASE_URL, VEHICLE_ID):
    # Variables
    DRIVER_SEAT_POSITION = GetDriverSeatPosition(BASE_URL, VEHICLE_ID)
    SEAT_HEATER_LEVEL = 0

    SetSeatHeater(BASE_URL, VEHICLE_ID, DRIVER_SEAT_POSITION, SEAT_HEATER_LEVEL)

  # Function that deactivates the front passenger's seat heater
  def StopFrontPassengerSeatHeater(BASE_URL, VEHICLE_ID):
    # Variables
    DRIVER_SEAT_POSITION = GetDriverSeatPosition(BASE_URL, VEHICLE_ID)
    SEAT_HEATER_LEVEL = 0
    if DRIVER_SEAT_POSITION == 0:
      FRONT_PASSENGER_SEAT_POSITION = 1
    else:
      FRONT_PASSENGER_SEAT_POSITION = 0
    
    SetSeatHeater(BASE_URL, VEHICLE_ID, FRONT_PASSENGER_SEAT_POSITION, SEAT_HEATER_LEVEL)

  # Function that activates the vehicle's sentry mode system
  def StartSentry(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'on': 1
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_sentry_mode"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's sentry mode system has been activated")
    else:
      print("ERROR: The vehicle failed to receive the start sentry mode system command")

  # Function that deactivates the vehicle's sentry mode system
  def StopSentry(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'on': 0
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_sentry_mode"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's sentry mode system has been deactivated")
    else:
      print("ERROR: The vehicle failed to receive the stop sentry mode system command")

  # Function that opens the vehicle's windows
  def OpenWindows(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'command': 'vent',
      'lat': 0,
      'lon': 0
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/window_control"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's windows have been opened")
    else:
      print("ERROR: The vehicle failed to receive the open windows command")

  # Function that closes the vehicle's windows
  def CloseWindows(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'command': 'close',
      'lat': 0,
      'lon': 0
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/window_control"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's windows have been closed")
    else:
      print("ERROR: The vehicle failed to receive the close windows command")

  # Function that actuates the vehicle's frunk
  def ActuateFrunk(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'which_trunk': 'front'
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/actuate_trunk"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's frunk has been actuated")
    else:
      print("ERROR: The vehicle failed to receive the actuate frunk command")

  # Function that actuates the vehicle's trunk
  def ActuateTrunk(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'which_trunk': "rear"
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/actuate_trunk"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's trunk has been actuated")
    else:
      print("ERROR: The vehicle failed to receive the actuate trunk command")

  # Function that sets the vehicle's charge limit
  def SetChargeLimit(BASE_URL, VEHICLE_ID, VEHICLE_CHARGE_LIMIT):
    # Variables
    DATA = {
      'percent': VEHICLE_CHARGE_LIMIT
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_charge_limit"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's charge limit has been set to " + VEHICLE_CHARGE_LIMIT + "%")
    else:
      print("ERROR: The vehicle failed to receive the set charge limit command")

  # Function that starts charging the vehicle
  def StartCharging(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/charge_start"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle has started charging")
    else:
      print("ERROR: The vehicle failed to receive the start charge command")

  # Function that starts charging the vehicle
  def StopCharging(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/charge_stop"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle has stopped charging")
    else:
      print("ERROR: The vehicle failed to receive the stop charge command")

  # Function that opens the charge port door
  def OpenChargePortDoor(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/charge_port_door_open"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's charge port door has been opened")
    else:
      print("ERROR: The vehicle failed to receive the open charge port door command")

  # Function that closes the charge port door
  def CloseChargePortDoor(BASE_URL, VEHICLE_ID):
    # Variables
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/charge_port_door_close"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's charge port door has been closed")
    else:
      print("ERROR: The vehicle failed to receive the close charge port door command")

  # Function that sets the vehicle's charge amps
  def SetChargingAmps(BASE_URL, VEHICLE_ID, VEHICLE_CHARGING_AMPS):
    # Variables
    DATA = {
      'charging_amps': VEHICLE_CHARGING_AMPS
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_charging_amps"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle's charging amps has been set to " + VEHICLE_CHARGING_AMPS + " amps")
    else:
      print("ERROR: The vehicle failed to receive the set charging amps command")

  # Function that enables scheduled charging
  def EnableScheduledCharging(BASE_URL, VEHICLE_ID, SCHEDULED_CHARGING_TIME):
    # Variables
    DATA = {
      'enable': 1,
      'time': SCHEDULED_CHARGING_TIME
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_scheduled_charging"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle has been configured to start charging at " + SCHEDULED_CHARGING_TIME)
    else:
      print("ERROR: The vehicle failed to receive the enable scheduled charging command")

  # Function that enables scheduled charging
  def DisableScheduledCharging(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'enable': 0
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_scheduled_charging"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle has been configured with scheduled charging disabled")
    else:
      print("ERROR: The vehicle failed to receive the disable scheduled charging command")

  # Function that disables scheduled charging
  def DisableScheduledCharging(BASE_URL, VEHICLE_ID):
    # Variables
    DATA = {
      'enable': 'false'
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/set_scheduled_charging"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("The vehicle has been configured with scheduled charging disabled")
    else:
      print("ERROR: The vehicle failed to receive the disable scheduled charging command")

  # Function that starts a remote drive session for the vehicle
  def StartRemoteDrive(BASE_URL, VEHICLE_ID, PASSWORD):
    # Variables
    DATA = {
      'password': str(PASSWORD)
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    URL = BASE_URL + VEHICLE_ID + "/command/remote_start_drive"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("A remote driving session has been started for the vehicle")
    else:
      print("ERROR: A remote driving session has failed to start for the vehicle")

  # Function that triggers HomeLink
  def TriggerHomeLink(BASE_URL, VEHICLE_ID):
    # Variables
    VEHICLE_DATA = GetVehicleLocation(BASE_URL, VEHICLE_ID)
    VEHICLE_LATITUDE = str(VEHICLE_DATA[0])
    VEHICLE_LONGITUDE = str(VEHICLE_DATA[1])
    HEADERS = {
      'Authorization': "Bearer " + TOKEN,
      'Content-Type': 'application/json',
      'User-Agent': 'None'
    }
    DATA = {
      'lat': VEHICLE_LATITUDE,
      'lon': VEHICLE_LONGITUDE
    }
    ENCODED_DATA = json.dumps(DATA).encode('utf-8')
    URL = BASE_URL + VEHICLE_ID + "/command/trigger_homelink"
    HTTP = urllib3.PoolManager()
    HTTP_REQUEST = HTTP.request(
      'POST',
      URL,
      headers=HEADERS,
      body=ENCODED_DATA
    )
    HTTP_REQUEST_STATUS_CODE = HTTP_REQUEST.status

    if HTTP_REQUEST_STATUS_CODE == 200:
      print("HomeLink has been triggered on the vehicle")
    else:
      print("ERROR: The vehicle failed to receive the trigger HomeLink command")

  def RunCommand(BASE_URL, VEHICLE_ID, INPUT_CMD, PARAMETER_1, PARAMETER_2):
    # Run the appropriate command based on the value of INPUT_CMD
    if INPUT_CMD == "test_command":
      TestFunction(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "lock_doors":
      LockDoors(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "unlock_doors":
      UnlockDoors(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "honk_horn":
      HonkHorn(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "flash_lights":
      FlashLights(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "start_climate_control" or INPUT_CMD == "start_hvac":
      StartClimateControl(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "set_temps":
      SetTemps(BASE_URL, VEHICLE_ID, PARAMETER_1)
    elif INPUT_CMD == "start_defrost":
      StartDefrost(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "stop_defrost":
      StopDefrost(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "start_driver_seat_heater":
      StartDriverSeatHeater(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "start_front_passenger_seat_heater":
      StartFrontPassengerSeatHeater(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "start_sentry":
      StartSentry(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "stop_sentry":
      StopSentry(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "open_windows" or INPUT_CMD == "vent_windows":
      OpenWindows(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "close_windows":
      CloseWindows(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "actuate_frunk":
      ActuateFrunk(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "actuate_trunk":
      ActuateTrunk(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "set_charge_limit":
      SetChargeLimit(BASE_URL, VEHICLE_ID, PARAMETER_1)
    elif INPUT_CMD == "start_charging":
      StartCharging(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "stop_charging":
      StopCharging(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "open_charge_port_door":
      OpenChargePortDoor(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "close_charge_port_door":
      CloseChargePortDoor(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "set_charging_amps":
      SetChargingAmps(BASE_URL, VEHICLE_ID, PARAMETER_1)    
    elif INPUT_CMD == "enable_scheduled_charging":
      EnableScheduledCharging(BASE_URL, VEHICLE_ID, PARAMETER_1)
    elif INPUT_CMD == "disable_scheduled_charging":
      DisableScheduledCharging(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "start_remote_drive":
      StartRemoteDrive(BASE_URL, VEHICLE_ID, PARAMETER_1)
    elif INPUT_CMD == "trigger_homelink":
      TriggerHomeLink(BASE_URL, VEHICLE_ID)
  # Macro commands
    elif INPUT_CMD == "start_climate_control_normal" or INPUT_CMD == "start_hvac_normal":
      SetTemps(BASE_URL, VEHICLE_ID, PARAMETER_1)
      StartClimateControl(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "start_climate_control_heat" or INPUT_CMD == "start_hvac_max":
      StartDefrost(BASE_URL, VEHICLE_ID)
      StartDriverSeatHeater(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "start_climate_control_heat_passenger" or INPUT_CMD == "start_hvac_max_spouse":
      StartDefrost(BASE_URL, VEHICLE_ID)
      StartDriverSeatHeater(BASE_URL, VEHICLE_ID)
      StartFrontPassengerSeatHeater(BASE_URL, VEHICLE_ID)
    elif INPUT_CMD == "stop_climate_control" or INPUT_CMD == "stop_hvac":
      StopDefrost(BASE_URL, VEHICLE_ID)
      StopDriverSeatHeater(BASE_URL, VEHICLE_ID)
      StopFrontPassengerSeatHeater(BASE_URL, VEHICLE_ID)
      StopClimateControl(BASE_URL, VEHICLE_ID)
    else:
      print("ERROR: " + INPUT_CMD + " is not a recognized command")

  ##################################################################################################################

  # Capture the INITIAL_VEHICLE_STATE to verify that the vehicle is awake
  if INITIAL_VEHICLE_STATE == "online" or INITIAL_VEHICLE_STATE == "testing":
    print("Sending the " + INPUT_CMD + " command to vehicle ID #" + VEHICLE_ID + " on behalf of " + CLIENT_IP_ADDRESS)
    RunCommand(BASE_URL, VEHICLE_ID, INPUT_CMD, PARAMETER_1, PARAMETER_2)
  else:
    print("Vehicle ID # " + VEHICLE_ID + " is currently " + INITIAL_VEHICLE_STATE)

    print("Sending the wake_up command to vehicle ID #" + VEHICLE_ID + " on behalf of " + CLIENT_IP_ADDRESS)
    WakeVehicle(BASE_URL, VEHICLE_ID)

    print("Sending the " + INPUT_CMD + " command to vehicle ID #" + VEHICLE_ID + " on behalf of " + CLIENT_IP_ADDRESS)
    RunCommand(BASE_URL, VEHICLE_ID, INPUT_CMD, PARAMETER_1, PARAMETER_2)
