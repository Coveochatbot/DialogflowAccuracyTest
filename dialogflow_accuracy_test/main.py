import dialogflow
import uuid


def main():
    project_id = 'accuracytestbot'
    parent = 'projects/{}/agent'.format(project_id)

    user_says_for_basic_find_intent_for_training_phrases = [
        'Hello',
        'Hi',
        'Good evening',
        'Good morning'
    ]
    user_says_for_detect_entity = [
        'I need help with my mouse',
        'My mouse is broken',
        'My mouse stopped working',
        'There is a bug with my mouse',
        'I need help with ASDFGT',
        'My ASDFGT is broken'
    ]
    user_says_for_detect_ambiguous_intent = [
        'I need help with hello',
        'Hello, I need help with my mouse',
        'Hi, my mouse is broken',
    ]
    user_says_for_detect_intent_with_typo = [
        'Helo',
        'I need hepl with my mouse',
        'Hi, my mouse is broke',
        'I needs help with my mouse',
    ]
    user_says_for_not_return_wrong_intent = [
        'Thank you',
        'Thanks',
        'Good bye',
        'Bye',
    ]
    user_says_for_dynamic_entities = [
        'What is the weather tomorrow?',
        'What is the weather today?',
        'What was the weather yesterday?',
        'What is the weather next week?',
        'What is the weather two days ago?'
    ]

    user_says_list = (
        user_says_for_basic_find_intent_for_training_phrases +
        user_says_for_detect_entity +
        user_says_for_detect_ambiguous_intent +
        user_says_for_detect_intent_with_typo +
        user_says_for_not_return_wrong_intent +
        user_says_for_dynamic_entities
    )
    assert(26 == len(user_says_list))

    responses = [get_chatbot_response(project_id, user_says) for user_says in user_says_list]
    with open('output', 'w') as file:
        print(responses, file=file)


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
