import dialogflow
import uuid


def main():
    project_id = 'accuracytestbot'
    session_id = str(uuid.uuid4())
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    message = 'Hello'
    response = get_chatbot_response(session_client, session, message)
    print_chatbot_response(response)


def get_chatbot_response(session_client, session, message):
    text_input = dialogflow.types.TextInput(
        text=message, language_code='en')
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response


def print_chatbot_response(response):
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))


if __name__ == '__main__':
    main()
