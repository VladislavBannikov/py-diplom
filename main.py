from VK import VK
from User import User
import json


def save_json_to_file(text ,filename='groups.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(text,ensure_ascii=False,indent=True))


if __name__ == "__main__":
    intro = "Проверка групп друзей VK. Введите ID или nickname для проверки.\n'k' - для генерации ссылки для получения токена\n'q' - выход "
    print(intro)

    while True:
        inp = input("Введите id пользователя или nickname:")
        # inp = '46743995'  # for test
        # inp = '1646659'  #blocked
        # inp = 'eshmargunov'
        if inp.lower() == 'k':
            print(VK.make_key_URL())
        elif inp.lower() == 'q':
            break
        else:
            try:
                print("Выполнение:", end='')
                user1 = User(user_id=inp)
                gr_info = user1.groups_has_but_friends_not()
                save_json_to_file(gr_info)
                print('Завершено')
            except Exception as e:
                print(e)
