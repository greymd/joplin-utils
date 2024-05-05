import requests
import hashlib
import os

api_endpoint = "http://localhost:41184"
token = os.getenv("JOPLIN_TOKEN")

def get_notes_and_check_duplicates():
    """Retrieve note data using pagination and check for duplicates"""
    page = 1
    has_more = True
    hash_dict = {}

    while has_more:
        url = f"{api_endpoint}/notes?fields=id,title,body&&order_by=updated_time&order_dir=DESC&limit=100&page={page}&token={token}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for note in data.get('items', []):
                hash_value = calculate_md5(note['title'], note['body'])
                if hash_value in hash_dict:
                    print(f"FOUND: Note ID {hash_dict[hash_value]} and Note ID {note['id']} have identical content.")
                else:
                    hash_dict[hash_value] = note['id']
            has_more = data.get('has_more', False)
            page += 1
        else:
            print("Failed to fetch data from the API. Status code:", response.status_code)
            break

def calculate_md5(title, body):
    """Generate an MD5 hash from the title and body of a note"""
    combined_text = title + body
    return hashlib.md5(combined_text.encode()).hexdigest()

def main():
    get_notes_and_check_duplicates()

if __name__ == "__main__":
    main()

