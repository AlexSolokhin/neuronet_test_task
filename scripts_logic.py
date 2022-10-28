from scripts_class import Dialog


nps_script = Dialog(states={'hello_logic': {
                                'intents': ['Да', 'Нет', 'Занят', 'Ещё раз']
                            },
                            'main_logic': {
                                'intents': ['Да', 'Нет', 'Не знаю', 'Возможно', 'Занят', 'Вопрос', 'Ещё раз'],
                                'entities': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                            },
                            'hangup_logic': {},
                            'forward_logic': {}
                            })


def dialog_func(result: NeuroNluRecognitionResult,
                script: Dialog,
                no_response_counter: int = 0,
                finished: bool = False) -> None:
    """
    Основная функция, содержащая логику скрипта.
    В зависимости от результата ответа пользователя и состояния инстанса вызывает следующее действие бота и получает новый результат.
    Вызывает себя же до тех пор, пока диалог не будет завершён.

    :param result: объект результата
    :param script: объект скрипта/диалога
    :param no_response_counter: счётчик ответов NONE/DEFAULT
    :param finished: флаг завершения диалога

    :return: None
    """

    if finished:
        nn.dialog.result = nn.RESULT_DONE
        nn.log('call_duration', nv.get_call_duration())
        nn.log('call_transcription', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))
        return

    if not result and script.cur_state == 'hello_logic' and no_response_counter == 0:
        no_response_counter += 1
        dialog_func(script.bot_action('hello_null'),
                    script,
                    no_response_counter,
                    finished)

    elif not result and script.cur_state == 'main_logic' and no_response_counter == 0:
        no_response_counter += 1
        dialog_func(script.bot_action('recommend_null'),
                    script,
                    no_response_counter,
                    finished)

    elif not result and no_response_counter == 1:
        finished = True
        dialog_func(script.bot_action('hangup_null', new_state='hangup_logic'),
                    script,
                    no_response_counter,
                    finished)

    elif script.cur_state == 'hello_logic':
        no_response_counter = 0
        cur_intent = None

        for intent in script.states[script.cur_state]['intents']:
            if result.has_intent(intent):
                cur_intent = intent

        if not cur_intent or cur_intent == 'Да':
            dialog_func(script.bot_action('recommend_main', new_state='main_logic'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Нет' or cur_intent == 'Занят':
            finished = True
            dialog_func(script.bot_action('hangup_wrong_time', new_state='hangup_logic'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Ещё раз':
            dialog_func(script.bot_action('hello_repeat'),
                        script,
                        no_response_counter,
                        finished)

    elif script.cur_state == 'main_logic':
        no_response_counter = 0
        cur_intent = None
        cur_entity = None

        for intent in script.states[script.cur_state]['intents']:
            if result.has_intent(intent):
                cur_intent = intent

        for entity in script.states[script.cur_state]['entities']:
            if result.has_intent(entity):
                cur_entity = entity

        if not cur_intent and not cur_entity and no_response_counter == 0:
            no_response_counter += 1
            dialog_func(script.bot_action('recommend_default'),
                        script,
                        no_response_counter,
                        finished)

        elif not cur_intent and not cur_entity and no_response_counter == 1:
            finished = True
            dialog_func(script.bot_action('hangup_null', new_state='hangup_logic'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_entity in {'8', '9', '10'}:
            no_response_counter = 0
            finished = True
            dialog_func(script.bot_action('hangup_positive', new_state='hangup_logic'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_entity in {'1', '2', '3', '4', '5', '6', '7'}:
            no_response_counter = 0
            finished = True
            dialog_func(script.bot_action('hangup_negative', new_state='hangup_logic'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Нет':
            no_response_counter = 0
            dialog_func(script.bot_action('recommend_score_negative'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Возможно':
            no_response_counter = 0
            dialog_func(script.bot_action('recommend_score_neutral'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Да':
            no_response_counter = 0
            dialog_func(script.bot_action('recommend_score_positive'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Ещё раз':
            no_response_counter = 0
            dialog_func(script.bot_action('recommend_repeat'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Не знаю':
            no_response_counter = 0
            dialog_func(script.bot_action('recommend_repeat_2'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Занят':
            finished = True
            dialog_func(script.bot_action('hangup_wrong_time', new_state='hangup_logic'),
                        script,
                        no_response_counter,
                        finished)

        elif cur_intent == 'Вопрос':
            finished = True
            dialog_func(script.bot_action('forward', new_state='forward_logic'),
                        script,
                        no_response_counter,
                        finished)
            # Какой-то метод для форварда на оператора
            nn.dialog.forward(free_operator)


if __name__ == '__main__':
    dialog_func(nps_script.bot_action('hello', new_state='hello_logic'),
                nps_script)
