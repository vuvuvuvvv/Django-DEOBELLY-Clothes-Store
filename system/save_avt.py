# import os
# import requests
# from clothes_shop.settings import STATIC_ROOT
# def save_avt(url, username,download = True):
#     response = requests.get(url)
#     folder_path = os.path.join(STATIC_ROOT,'images/users/',username)

#     # Check if the folder already exists
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
        
#     if response.status_code == 200:
#         image_data = response.content
#         print(image_data)
#         image_name = os.path.basename(url)  # Extract image name from URL
#         image_path = os.path.join(folder_path, image_name)
        
#         with open(image_path, 'wb') as image_file:
#             image_file.write(image_data)
        
#         return True, image_path
#     else:
#         return False, None