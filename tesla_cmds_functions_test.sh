#!/bin/bash
# Filename:             tesla_cmds_functions_test.sh
# By:                   Dan Burkland
# Date:                 2020-12-14
# Purpose:              Validates the latest build of the Tesla CMDs functions. This is meant to be used in a CI/CD pipeline.
# Version:              1.2

# Variables
FUNCTION_URL="$1"
TESLA_TOKEN="$2"
VEHICLE_ID="$3"
INPUT_CMD="$4"

# Generate Curl Request Body
generate_curl_body() {
  cat <<EOF
{
  "TOKEN": "${TESLA_TOKEN}",
  "VEHICLE_ID": "${VEHICLE_ID}",
  "INPUT_CMD": "${INPUT_CMD}",
  "PARAMETER_1": "69",
  "PARAMETER_2": "69"
}
EOF
}

# Validate the front-end function
CURL_OUTPUT=$(curl -s -o /dev/null -w "%{http_code}" --location --request POST $FUNCTION_URL --header 'Content-Type: application/json' --data-raw "$(generate_curl_body)")

# Exit script with proper status code based on the test result
if [ "$CURL_OUTPUT" -eq "200" ]; then
  echo "tesla_cmds_aws_lambda_functions build test result: PASSED"
  exit 0
else
  echo "tesla_cmds_aws_lambda_functions build test result: FAILED"
  exit 1
fi
