# файл, в котором будут вся логика, которая будет дергаться из вешних фуункций бота
import collections
import re
import pymorphy2

def add_item_to_wishllist(user_id, url, name, users_lists):
    '''
        user_id - ID юзера в телеге, уникальный параметр
        name - навзвание товара, например зеленые валенки
        url - ссылка, например https://www.wildberries.ru/catalog/17864232/detail.aspx
        
        добавляем в мару users_lists "url name" по ключу user_id
        в будущем это будет загрузка в удаленную бд

    '''
    line = url + ' ' + name
    if user_id not in users_lists:
        users_lists[user_id] = {line} #используем collections.set
    else:
        users_lists[user_id].add(line)

def remove_item_from_wishlist(user_id, url, name, users_lists):
    '''
    как добавить, только удалить, и надо возвращать bool, был ли товар в вишлисте вообще
    '''
    pass


def find_colors_and_clothing(sentence):
    colors = ['красн', 'оранжев', 'желт', 'зелен', 'голуб', 'син', 'фиолет', 'розов', 'черн', 'бел', 'сер', 'коричнев']
    clothing = ['рубашк', 'блузк', 'футболк', 'свитер', 'пиджак', 'пальт', 'плать', 'юбк', 'брюк', 'джинс', 'шорт', 'пояс', 'шарф', 'платок', "шляп", "штан"]

    # Находим все слова в предложении
    words = re.findall(r'\w+', sentence)

    morph = pymorphy2.MorphAnalyzer()

    colors_found = []
    clothing_found = []

    for word in words:
        normal_form = morph.parse(word)[0].normal_form

        for color in colors:
            if normal_form.startswith(color):
                colors_found.append(word)

        for item in clothing:
            if normal_form.startswith(item):
                clothing_found.append(word)

    return colors_found, clothing_found

def tune_text(text):
    clothes = []
    colors = []
    sex = ["муж", "жен"]
    colors, clothes = find_colors_and_clothing(text)
    if "мужч" in text or "мужс" in text.lower():
        text = "мужской " + " ".join(colors) + " " + " ".join(clothes)
    elif "женщ" in text or "женс" in text.lower():
        text = "женский " + " ".join(colors) + " " + " ".join(clothes)
    else:
        text = " ".join(colors) + " " + " ".join(clothes)
    return text


# users_list = {}
# add_item_to_wishllist("kleickik", "http://smth", "ничего", users_list)
# assert len(users_list["kleickik"]) == 1
# add_item_to_wishllist("kleickik", "http://smth", "ничего", users_list)
# assert len(users_list["kleickik"]) == 1
# add_item_to_wishllist("kleickik", "http://smth1", "ничего", users_list)
# assert len(users_list["kleickik"]) == 2