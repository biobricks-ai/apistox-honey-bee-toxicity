import requests
import os
import sys

def download_data():
    record_id = "11062076"
    api_url = f"https://zenodo.org/api/records/{record_id}"
    
    print(f"Fetching metadata from {api_url}")
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch record metadata: {response.status_code}")
        sys.exit(1)
        
    data = response.json()
    files = data.get('files', [])
    
    if not files:
        print("No files found in record.")
        sys.exit(1)
        
    # Look for the main dataset file (likely a CSV or Excel)
    target_file = None
    for f in files:
        if f['key'].endswith('.csv') or f['key'].endswith('.xlsx'):
            target_file = f
            break
            
    if not target_file:
        print("No CSV/XLSX found, listing all files:")
        for f in files:
            print(f['key'])
        target_file = files[0]
        
    download_url = target_file['links']['self']
    filename = target_file['key']
    
    # Ensure download directory exists
    if not os.path.exists("download"):
        os.makedirs("download")
        
    output_path = os.path.join("download", filename)
    
    print(f"Downloading {filename} from {download_url}")
    
    file_response = requests.get(download_url, stream=True)
    if file_response.status_code != 200:
        print(f"Failed to download file: {file_response.status_code}")
        sys.exit(1)
        
    with open(output_path, 'wb') as f:
        for chunk in file_response.iter_content(chunk_size=8192):
            f.write(chunk)
            
    print(f"Downloaded to {output_path}")

if __name__ == "__main__":
    download_data()
