import random


def get_username():
    with open('sayIt_usernames.txt', mode='r+') as usernames_file:
        names_list = [name.strip() for name in usernames_file.readlines()]
        if names_list:
            name_picked = random.choice(names_list)
            names_list.remove(name_picked)
            usernames_file.seek(0)
            for name in names_list:
                usernames_file.write(f'{name}\n')
            usernames_file.truncate()
            return name_picked, True  # add soem true/false logic here to check if name was actually returned
        else:
            return 'Give us a minute, no usernames available for now.', False
