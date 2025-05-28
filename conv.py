import requests
import re

print("\nTHIS IS A KQT PRODUCTION\n")

def is_valid_username(name):
    return (
        3 <= len(name) <= 16 and
        re.fullmatch(r'[A-Za-z0-9_]+', name) is not None
    )

def read_usernames(filename):
    with open(filename, 'r') as file:
        raw = {line.strip() for line in file if line.strip()}
        valid = [name for name in raw if is_valid_username(name)]
        invalid = raw - set(valid)
        for name in invalid:
            print(f"Skipping invalid username: {name}")
        return valid

def get_uuid(name):
    url = f"https://playerdb.co/api/player/minecraft/{name}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["success"]:
            return data["data"]["player"]["id"]
        else:
            return None
    except Exception as e:
        print(f"Error fetching {name}: {e}")
        return None

if __name__ == "__main__":
    usernames = read_usernames("usernames.txt")

    with open("uuids.txt", "w") as out_file, open("not_found.txt", "w") as not_found_file:
        for i, name in enumerate(usernames):
            uuid = get_uuid(name)
            if uuid:
                out_file.write(f"{name}: {uuid}\n")
                print(f"[{i+1}/{len(usernames)}] {name}: {uuid}")
            else:
                not_found_file.write(f"{name}\n")
                print(f"[{i+1}/{len(usernames)}] {name}: not found")
