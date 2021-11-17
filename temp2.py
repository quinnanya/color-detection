import json
import requests
with open ("manifest4.json", "r") as f:
    data = json.load(f)

def get_images(url):
	s = requests.get(url).text
	data = json.loads(s)
	seq = data['sequences'][0]['canvases']
	for item in seq:
		print(item['images'][0]['@id'])

seq = data["sequences"][0]["canvases"]
for item in seq:
    url = item['images'][0]['resource']['@id']
    print (url)
    # get_images(url)
        # url = item["@id"]+"/full/1200,/0/default.jpg?t=1603129222086.jpg"
