import random
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def get_username():
    with open('sayIt_usernames.txt', mode='r+', encoding='utf-8') as usernames_file:
        names_list = [name.strip() for name in usernames_file.readlines()]
        if names_list:
            name_picked = random.choice(names_list)
            names_list.remove(name_picked)
            usernames_file.seek(0)
            for name in names_list:
                usernames_file.write(f'{name}\n')
            usernames_file.truncate()
            return name_picked, True
        else:
            return 'Give us a minute, no usernames available for now.', False


def call_api_based_on_category(category):
    top_headlines_url = 'https://newsapi.org/v2/top-headlines?'
    params = {
        'apiKey': os.getenv('NEWS_API_KEY'),
        'category': category,
    }

    response = requests.get(top_headlines_url, params).json()
    article = response['articles'][0]
    print(article)
    mapped = {
        category: {
            'headline': article['title'],
            'description': article['description'],
            'url': article['url']
                   }
    }
    print(mapped)
# if __name__ == "__main__":
#     call_api_based_on_category('sports')


