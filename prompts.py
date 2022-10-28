from config import db, media_params, default_env


def get_prompt(prompt_name: str, lang: str = media_params['lang'], flag: str = default_env['flag']) -> PromptObject:
    """
    Функция для извлечения промта из БД по имени.
    Для примера использовал синтаксис ORM Peewee как максимально простой и понятный.
    Вероятным отношением ManyToMany с параметрами lang и flag принебрёг также для упрощения.

    :param prompt_name: имя промта
    :param lang: язык (дефолтно из конфига)
    :param flag: флаг (дефолтно из конфига)
    :return:
    """

    with db:
        prompt = PromptsTable.get(name=prompt_name).where(lang == lang, flag == flag)
        promt_obj = prompt.promt_obj
        return promt_obj