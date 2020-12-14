README
=========

### Introduction

Tesla Commands (CMDs) is a set of AWS Lambda Functions that serve as an intelligent wrapper around Tesla's API. These functions are designed for a set of iOS shortcuts however support any application that can issue REST API calls. 

### Supported Commands

* actuate_frunk
* actuate_trunk
* start_climate_control_normal or start_hvac_normal
* start_climate_control_heat or start_hvac_max
* start_climate_control_heat_passenger or start_hvac_max_spouse
* stop_climate_control or stop_hvac
* lock_doors
* unlock_doors
* start_sentry
* stop_sentry
* open_windows or vent_windows
* close_windows
* set_charge_limit
* open_charge_port_door
* close_charge_port_door
* start_charging
* stop_charging
* honk_horn
* flash_lights
* start_remote_drive
* trigger_homelink

### FAQs

* What does each command do?
  * Please refer to the Tesla iOS Shortcuts [README](https://github.com/dburkland/tesla_ios_shortcuts/blob/master/README.md)
* At a high level, how does the Tesla CMDs API service work?
  * iOS Shortcut -> AWS API Gateway -> Front-end AWS Lambda Function -> AWS SNS -> Back-end AWS Lambda Function -> Tesla API Service
