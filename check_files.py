import requests
def list_files():
    record_id = "11062076"
    api_url = f"https://zenodo.org/api/records/{record_id}"
    response = requests.get(api_url)
    data = response.json()
    files = data.get('files', [])
    for f in files:
        print(f"{f['key']} : {f['size']} bytes")

if __name__ == "__main__":
    list_files()
