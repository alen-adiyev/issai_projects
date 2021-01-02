import requests

url = 'https://cdn.kitap.kz/storage/audiobook/442/track_0.mp3'
r = requests.get(url, allow_redirects=True)

open('399_00' + '.wav', 'wb').write(r.content)

# for i in range (5, 37):
#     try:
#         url = 'https://cdn.kitap.kz/storage/audiobook/4742/track_' + str(i) + '.mp3'
#         r = requests.get(url, allow_redirects=True)
#         print("got url")
        
#         if i < 10:
#             open('025_0' + str(i) + '.wav', 'wb').write(r.content)
#         else:
#             open('025_' + str(i) + '.wav', 'wb').write(r.content) 
        
#         print ("downloaded")
#     except Exception:
#         print("finished")
#         break