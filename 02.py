import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter

import matplotlib.pyplot as plt
import requests


def get_text(url):                                                      # Функція отримання тексту з URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:                   # Обробляємо помилки, якщо виникають
        print(f"Error fetching the text from {url}: {e}")
        return ""


def remove_punctuation(text):                                           # Функція для видалення знаків пунктуації
   return text.translate(str.maketrans("", "", string.punctuation))     # Повертаємо текст без символів пунктуації


def map_function(word):                                                 # Функція маппінгу, що перетворює кожне слово на (слово, 1)
    return word, 1


def shuffle_function(mapped_values):                                    # Функція для групування (shuffle) значень за ключами
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()                                             # Повертаємо словник, де кожен ключ містить список відповідних значень


def reduce_function(key_values):                                        # Функція редукції, що підсумовує кількість входжень кожного ключа
    key, values = key_values
    return key, sum(values)                                             # Повертаємо пару (ключ, підсумовані значення)


def map_reduce(text, search_words=None):                                # Основна функція для виконання процесу MapReduce, що
                                                                        # виконує mapping, shuffle та reduction
    text = remove_punctuation(text)
    words = text.split()                                                # Повертаємо словник зі словами та їхньою частотою

    
    if search_words:                                                    # Якщо задано список слів для пошуку, враховувати тільки ці слова
        words = [word for word in words if word in search_words]

    with ThreadPoolExecutor() as executor:                              # Крок 1: Маппінг
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)                   # Крок 2: Групування

    with ThreadPoolExecutor() as executor:                              # Крок 3: Редукція
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(result, top_n=15):                              # Функція для візуалізації результатів top-15 слів за частотою
    top_words = Counter(result).most_common(top_n)                      # Визначення top-15 найчастіше використовуваних слів

    words, counts = zip(*top_words)                                     # Ділимо дані на слова та їх частоти

    plt.figure(figsize=(10, 6))                                         # Створюємо графік
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top {} Most Frequent Words'.format(top_n))
    plt.gca().invert_yaxis()                                            # Перевертаємо графік, щоб найбільші значення були зверху
    plt.show()


if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks/fr100202.txt"                # Вхідний текст для обробки
    text = get_text(url)
    
    result = map_reduce(text)                                           # Виконуємо MapReduce на вхідному тексті
    
    visualize_top_words(result)                                         # Візуалізуємо результати