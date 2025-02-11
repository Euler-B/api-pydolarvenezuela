import os
import json
import cloudinary
from dotenv import load_dotenv
# from cloudinary.search import Search
from cloudinary.uploader import upload
from manifest import PAGES

load_dotenv('./.env')

CLOUD_NAME = os.getenv("CLOUD_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

cloudinary.config(
    cloud_name = CLOUD_NAME,
    api_key = API_KEY,
    api_secret = API_SECRET
)

def upload_image(file: bytes, public_id: str, folder: str) -> str:
    upload_result = upload(file, public_id=public_id, folder=folder)
    return upload_result["secure_url"]

if __name__ == "__main__":
    images = {}
    data = []
    for page in PAGES:
        for file in page["files"]:
            # search = Search().expression(f"public_id:{os.path.basename(file['file']).split('.')[0]}").execute()
            # if search["total_count"] > 0:
            #     url = search["resources"][0]["secure_url"]
            #     print(f"Image {file['title']} already exists: {url}")
            if images.get(file["title"]):
                print(f"Image {file['title']} already exists: {images[file['title']]}")
                url = images[file["title"]]
            else:
                with open(f"./icons/webp/{file['file']}", "rb") as image:
                    url = upload_image(image.read(), f'public_id:{os.path.basename(file['file']).split('.')[0]}', 'monitors')
                    images[file["title"]] = url
                    print(f"Uploaded {file['title']}: {url}")

            data.append({
                "provider": page["page"],
                "title": file["title"],
                "image": url
            })
    with open("data.json", "w") as f:
        f.write(json.dumps(data, indent=4))
