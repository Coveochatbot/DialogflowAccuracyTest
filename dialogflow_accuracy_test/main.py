import apiai
import argparse
import json
import uuid


def main():
    dialogflow_client_access_token = get_dialogflow_client_access_token()
    session_id = str(uuid.uuid4())

    chatbot = apiai.ApiAI(dialogflow_client_access_token)

    user_says = 'Hello'
    json_response = get_json_response(chatbot, session_id, user_says)
    intent = json_response_to_intent(json_response)
    speech = json_response_to_speech(json_response)
    answer_summary = 'user says: "{}" => intent: "{}", speech: "{}"'.format(user_says, intent, speech)
    print(answer_summary)


def json_response_to_intent(json_response):
    return json_response['result']['metadata']['intentName']


def json_response_to_speech(json_response):
    return json_response['result']['fulfillment']['speech']


def get_json_response(chatbot, session_id, user_says):
    request = chatbot.text_request()
    request.session_id = session_id
    request.query = user_says
    http_response = request.getresponse()
    response_content = http_response.read()
    decoded_response = response_content.decode()
    json_response = json.loads(decoded_response)
    return json_response


def get_dialogflow_client_access_token():
    parser = argparse.ArgumentParser(description='Process program arguments')
    parser.add_argument('--dialogflow_client_access_token', type=str,
                        help='DialogFlow client access token')
    args = parser.parse_args()
    return args.dialogflow_client_access_token


if __name__ == '__main__':
    main()
