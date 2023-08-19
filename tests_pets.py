# Импорт необходимых библиотек и модулей
from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Фикстура для инициализации и завершения тестов
@pytest.fixture(autouse=True)
def testing():
    # Инициализация драйвера Chrome
    pytest.driver = webdriver.Chrome()

    # Настройка неявного ожидания для элементов
    pytest.driver.implicitly_wait(10)

    # Открытие страницы для авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.maximize_window()

    # Ввод данных для авторизации
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')

    # Нажатие на кнопку "Войти" с использованием явного ожидания
    WebDriverWait(pytest.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # Нажатие на ссылку "Мои питомцы" с использованием явного ожидания
    WebDriverWait(pytest.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Мои питомцы')]"))).click()

    # Действия выполняются перед началом выполнения тестов
    yield

    # Завершение тестов: закрытие браузера
    pytest.driver.quit()

"""Тест: проверка, что колличество питомцев совпадает с ожидаемым результатом"""

"""Тест проходт, колличество совпадает"""

def test_all_pets_present():
    # Ожидание появления списка питомцев
    pytest.driver.implicitly_wait(10)

    # Получение списка строк, представляющих питомцев
    Nline = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')

    # Получение количества питомцев из текста страницы
    NPets = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())

    # Сравнение количества питомцев и строк в списке
    assert NPets == len(Nline)


"""Тест: проверка, что у половины питомцев есть фото"""

"""Тест не падает значит у половины питомцев есть фото"""

def test_half_pets_with_photo():
    # Ожидание появления списка фотографий
    pytest.driver.implicitly_wait(10)

    # Получение списка изображений питомцев
    images = pytest.driver.find_elements(By.TAG_NAME, 'img')

    # Получение количества питомцев из текста страницы
    NPets = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())

    # Подсчет питомцев без фотографий
    No_images = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') == "":
            No_images += 1

    # Проверка, что количество питомцев без фотографий не превышает половину от общего количества питомцев
    assert NPets / 2 >= No_images

"""Тест: проверка, что у всех питомцев есть имя, возраст и порода"""

"""Тест не падает у всех питомцев есть имя, возраст и порода"""

def test_all_pets_have_name_ages_breed():
    # Ожидание появления списка питомцев
    pytest.driver.implicitly_wait(10)

    # Получение количества питомцев из текста страницы
    NPets = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())

    # Получение списков имён, пород и возрастов питомцев
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')

    # Проверка, что для каждого питомца указаны имя, порода и возраст
    for i in range(len(names)):
        assert names[i].text != ""
        assert breed[i].text != ""
        assert ages[i].text != ""

    # Проверка, что общее количество питомцев соответствует количеству указанных имён, пород и возрастов
    assert NPets == len(names) == len(breed) == len(ages)

"""Тест: проверка, что все имена питомцев различны"""

"""Тест падает значит есть повторяющиеся имена"""

def test_all_names_different():
    # Ожидание появления списка питомцев
    pytest.driver.implicitly_wait(10)

    # Получение списка имён питомцев
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    list_of_names = []

    # Запись всех имён в список
    for i in range(len(names)):
        list_of_names.append(names[i].text)

    # Создание множества уникальных имён
    unique_names = set(list_of_names)

    # Проверка, что количество всех имён равно количеству уникальных
    assert len(list_of_names) == len(unique_names)

"""Тест: проверка отсутствия повторяющихся питомцев"""

"""Тест падает - значит есть повторяющиеся питомцы"""

def test_no_repeating_pets():
    # Ожидание появления списка питомцев
    pytest.driver.implicitly_wait(10)

    # Получение списков имён, пород и возрастов питомцев
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')

    # Создание списков для хранения имён, пород и возрастов
    list_names = []
    list_breed = []
    list_ages = []
    list_pets = []
    spisok = []

    # Заполнение списков значениями из таблицы
    for i in range(len(names)):
        list_names.append(names[i].text)
        list_breed.append(breed[i].text)
        list_ages.append(ages[i].text)

    # Создание списка для хранения питомцев и их характеристик
    for j in range(len(names)):
        list_pets.append(list_names[j])
        list_pets.append(list_breed[j])
        list_pets.append(list_ages[j])
        spisok.append(list_pets)
        list_pets = []

    # Проверка отсутствия повторяющихся питомцев
    for k in range(len(names)):
        n = k + 1
        while n < len(names):
            assert spisok[k] != spisok[n]
            n += 1  # Завершение цикла проверки повторяющихся питомцев

if __name__ == "__main__":
    pytest.main()