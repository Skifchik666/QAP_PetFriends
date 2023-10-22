from api import PetFriends
from settings import (valid_email, valid_password, invalid_email,
                      invalid_password, empty_email, empty_password, long_name, invalid_key)
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
       запрашиваем список всех питомцев и проверяем что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='Копибара', age='6', pet_photo='images/1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo(name='Барбоскин', animal_type='двортерьер', age='4'):
    """Проверка добавления информации о питомце без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pets(pet_photo='images/1.jpg'):
    """Проверка добавления фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_photo_of_pets(auth_key, pet_id, pet_photo)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']

def test_get_api_key_for_invalid_user(email = invalid_email, password=invalid_password):
    """ Проверяем что ключ не получен при неправильном вводе Email, Password"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_age(name='Барбоскин', animal_type='двортерьер', age='999'):
    """Проверка добавления информации о питомце с слишком большим возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['age'] == '999'

def test_add_new_pet_not_name(name=' ', animal_type='двортерьер', age='7'):
    """Проверка добавления информации о питомце без имени"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == ' '

def test_add_new_pet_not_animal_type(name='Персик', animal_type='', age='7'):
    """Проверка добавления информации о питомце без имени"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['animal_type'] == ''

def test_add_new_pet_invalid_photo(name='Левша', animal_type='Копибара', age='6', pet_photo='images/2.txt'):
    """Проверяем что можно добавить питомца с текстовым файлом вместо фото,
    питомец добавится но без фото"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['pet_photo'] == ''

def test_get_api_key_for_empty_user(email = empty_email, password=empty_password):
    """ Проверяем что ключ не получен, при отправке пустых полей Email, Password"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_long_name(name = (long_name), animal_type='двортерьер', age='4'):
    """Проверка добавления питомца с длинным именем"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос не возвращает список питомцев при неправельном key """

    auth_key = invalid_key

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'my_pets' not in result

