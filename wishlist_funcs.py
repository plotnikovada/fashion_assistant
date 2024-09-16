# файл, в котором будут вся логика, которая будет дергаться из вешних фуункций бота
import collections

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

users_list = {}
add_item_to_wishllist("kleickik", "http://smth", "ничего", users_list)
assert len(users_list["kleickik"]) == 1
add_item_to_wishllist("kleickik", "http://smth", "ничего", users_list)
assert len(users_list["kleickik"]) == 1
add_item_to_wishllist("kleickik", "http://smth1", "ничего", users_list)
assert len(users_list["kleickik"]) == 2