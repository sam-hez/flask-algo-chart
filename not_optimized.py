def remove_duplicate_users(users):
    unique_users = []

    for i in range(len(users)):
        seen = False
        for j in range(len(unique_users)):
            if users[i]['id'] == unique_users[j]['id']:
                seen = True
                break
        if not seen:
            unique_users.append(users[i])

    return unique_users


if __name__ == "__main__":
    users = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 2}]
    print(remove_duplicate_users(users))
