import requests
import re
import time

print("\nTHIS IS A KQT PRODUCTION\n")

def is_valid_username(name):
    return (
        3 <= len(name) <= 16 and
        re.fullmatch(r'[A-Za-z0-9_]+', name) is not None
    )

def read_usernames_from_file(filename):
    with open(filename, 'r') as file:
        raw = {line.strip() for line in file if line.strip()}
        valid = [name for name in raw if is_valid_username(name)]
        invalid = raw - set(valid)
        for name in invalid:
            print(f"Skipping invalid username: {name}")
        return valid

def get_uuid_for_name(name, max_retries=5):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    retries = 0
    wait_time = 1

    while retries <= max_retries:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['id']
        elif response.status_code == 204:
            return None
        elif response.status_code == 429:
            print(f"Rate limited. Retrying {name} in {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
            wait_time *= 2
        else:
            print(f"Error {response.status_code} for {name}")
            return None
    print(f"Failed to fetch {name} after {max_retries} retries.")
    return None

if __name__ == "__main__":
    usernames = read_usernames_from_file("usernames.txt")

    with open("uuids.txt", "w") as out_file, open("not_found.txt", "w") as not_found_file:
        for i, name in enumerate(usernames):
            uuid = get_uuid_for_name(name)
            if uuid:
                out_file.write(f"{name}: {uuid}\n")
                print(f"[{i+1}/{len(usernames)}] {name}: {uuid}")
            else:
                not_found_file.write(f"{name}\n")
                print(f"[{i+1}/{len(usernames)}] {name}: not found")
            time.sleep(1)