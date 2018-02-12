import dialogflow
import uuid


def main():
    project_id = 'accuracytestbot'
    parent = 'projects/{}/agent'.format(project_id)
    session_id = str(uuid.uuid4())
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    message = 'Hello'
    response = get_chatbot_response(session_client, session, message)
    print_chatbot_response(response)

    delete_all_intents(parent)
    assert(0 == get_number_of_intents(parent))

    intents_to_create = [
        {
            'display_name': 'best_university',
            'training_phrases_parts': [
                'what is the best university?',
                'what is the greatest university?',
                'where should I study?',
                'can you recommend me an university?'
            ],
            'message_texts': [
                'Sherby',
                'Sherbrooke',
                'Université de Sherbrooke',
                'UdeS'
            ]
        },
        {
            'display_name': 'best_poutine',
            'training_phrases_parts': [
                'who makes the greatest poutine?',
                'who makes the best poutine?',
                'where is the greatest poutine?',
                'where is the best poutine?'
            ],
            'message_texts': [
                'Snack bar Cameleon',
                'The Snack',
                'The Cameleon',
                'That poutine place on Galt street'
            ]
        }
    ]
    create_intents_from_intent_dicts(parent, intents_to_create)
    assert(2 == get_number_of_intents(parent))


def create_intent(parent, display_name, training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    intents_client.create_intent(parent, intent)


def create_intents_from_intent_dicts(parent, intent_dicts):
    for intent_dict in intent_dicts:
        create_intent_from_intent_dict(parent, intent_dict)


def create_intent_from_intent_dict(parent, intent_dict):
    create_intent(
        parent,
        intent_dict['display_name'],
        intent_dict['training_phrases_parts'],
        intent_dict['message_texts']
    )


def get_number_of_intents(parent):
    return len(list(get_all_intents(parent)))


def get_all_intents(parent):
    intents_client = dialogflow.IntentsClient()
    return intents_client.list_intents(parent)


def delete_all_intents(parent):
    intents = get_all_intents(parent)
    intents_client = dialogflow.IntentsClient()
    intents_client.batch_delete_intents(parent, intents)


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
