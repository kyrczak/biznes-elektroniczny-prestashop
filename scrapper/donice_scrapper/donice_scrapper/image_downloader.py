import os
import requests
import time
from urllib.parse import urlparse
import json
from concurrent.futures import ThreadPoolExecutor

def download_image(product_id, image_url, download_path, timestamp, image_index):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Create the directory if it doesn't exist
        directory_path = os.path.join(download_path, str(product_id))
        os.makedirs(directory_path, exist_ok=True)

        #save the image to directory_path + the part after / in the url
        image_path = os.path.join(directory_path, f'{image_url}')
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Image {image_index + 1}/{len(image_url)} downloaded successfully.")
    else:
        print(f"Failed to download image {image_index + 1}/{len(image_url)}. Status code: {response.status_code}")

def download_images(download_path='../../results/images/full/', num_threads=8):
    with open ('../../results/products.json', 'r') as json_file:
        product_data = json.load(json_file)
    
    cnt = 0
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for product in product_data:
            product_id = product['id']
            image_url = product['image_urls']
            timestamp = int(time.time())
            for image_index in range(len(image_url)):
                executor.submit(download_image, product_id, image_url[image_index], download_path, timestamp, image_index)
            cnt += 1
            print(f"Product {cnt}/{len(product_data)} downloaded successfully.")

if __name__ == "__main__":
    download_images()