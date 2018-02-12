import dialogflow
import uuid


def main():
    project_id = 'accuracytestbot'
    parent = 'projects/{}/agent'.format(project_id)
    message = 'Hello'
    response = get_chatbot_response(project_id, message)
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

    accuracy_tests = [
        {
            'user_says': "What is the best university?",
            'expected_intent': 'best_university'
        },
        {
            'user_says': "What is the greatest university?",
            'expected_intent': 'best_university'
        },
        {
            'user_says': "Who makes the best poutine??",
            'expected_intent': 'best_poutine'
        },
        {
            'user_says': "Where is the best poutine?",
            'expected_intent': 'best_poutine'
        },
        {
            'user_says': "Very tough question, impossible to get intent",
            'expected_intent': 'best_university'
        }
    ]
    accuracy_test_results = run_accuracy_tests(project_id, accuracy_tests)
    nb_passing_tests = len(accuracy_test_results['passing_tests'])
    nb_failing_tests = len(accuracy_test_results['failing_tests'])
    nb_total_tests = nb_passing_tests + nb_failing_tests
    accuracy_ratio = float(nb_passing_tests) / float(nb_total_tests)
    print('Accuracy ratio: {} / {} = {}'.format(nb_passing_tests, nb_total_tests, accuracy_ratio))
    assert(4 == nb_passing_tests)
    assert(1 == nb_failing_tests)
    assert(0.8 == accuracy_ratio)


def run_accuracy_tests(project_id, accuracy_tests):
    passing_tests = []
    failing_tests = []
    for accuracy_test in accuracy_tests:
        if is_passing_accuracy_test(project_id, accuracy_test):
            passing_tests.append(accuracy_test)
        else:
            failing_tests.append(accuracy_test)
    return {'passing_tests': passing_tests, 'failing_tests': failing_tests}


def is_passing_accuracy_test(project_id, accuracy_test):
    response = get_chatbot_response(project_id, accuracy_test['user_says'])
    intent = response.query_result.intent.display_name
    return accuracy_test['expected_intent'] == intent


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


def get_chatbot_response(project_id, message):
    session_id = str(uuid.uuid4())
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
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
