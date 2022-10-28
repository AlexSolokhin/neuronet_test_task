from typing import Dict, Optional
from prompts import get_prompt


class Dialog:
    """
    Класс для описания скрипта/диалога.
    Содержит словарь со стэйтами (логическими блоками) скрипта и набор entities и intents для каждого
    """

    def __init__(self, states: Optional[Dict] = None) -> None:
        self.states = states
        self.cur_state: Optional[str] = None

    def set_state(self, state_name: str) -> None:
        """
        Метод изменяет текущий стейт

        :param state_name: новый стэйт
        :return: None
        """

        if state_name in self.states:
            self.cur_state = self.states[state_name]

    def listen_user_intent(self) -> Optional[NeuroNluRecognitionResult]:
        """
        Метод слушает пользователя и возвращает объект результата или ничего.
        Параметры определяются состояниям инстанса.

        :return: объект результата
        :rtype: None or NeuroNluRecognitionResult
        """
        entities = self.cur_state.get('entities', None)
        intents = self.cur_state.get('intents', None)

        with nv.listen(detect_policy=(stop_enteties, stop_intents),
                       enteties=entities,
                       intents=intents) as user_response:
            if len(user_response) == 0:
                return None
            else:
                result = nlu.extract(user_response, entities, intents)
            return result

    def bot_action(self, prompt_name: str, new_state: Optional[str] = None) -> Optional[NeuroNluRecognitionResult]:
        """
        Метод включает в себя один обмен репликами с пользователем: реплика бота + фиксация ответа пользователя.

        :param prompt_name: имя промпта, который должен произнести бот.
        :param new_state: новый стэйт, который необходимо назначить инстансу

        :return: объект результата
        :rtype: None or NeuroNluRecognitionResult
        """

        if new_state:
            self.set_state(new_state)

        prompt = get_prompt(prompt_name)
        nv.say(prompt)

        result = self.listen_user_intent()
        return result
