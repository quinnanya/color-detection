# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import streamlit as st
import pandas as pd
import numpy as np
import argparse
import cv2
import json
import requests
from PIL import Image
import io


def get_images(url):
	s = requests.get(url).text
	data = json.loads(s)
	seq = data['sequences'][0]['canvases']
	num = len(seq)
	images  = []
	my_bar = st.progress(0)
	i=0
	tick = 100//num
	for item in seq:
		my_bar.progress(i+tick)
		image_url = item['images'][0]['resource']['@id']
		image = Image.open(requests.get(image_url, stream=True).raw)
		# image = cv2.imdecode(image, 3)
		# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# st.image(image)
		images.append(image)
		i=i+tick
	return (images)


# define the list of boundaries
# Don't forget BGR
st.sidebar.header("Parameters")
boundary_style = st.sidebar.selectbox("Boundary Style",
						("Standard Boundaries", "Custom Boundaries")
						)
image_location = st.sidebar.selectbox("Image Location", ("Local", "IIIF"))
form = st.sidebar.form("boundary form")
if image_location == 'Local':
	file = form.file_uploader('Upload a photo')

elif image_location == 'IIIF':
	url = form.text_input("URL")


if boundary_style == "Standard Boundaries":
	boundaries = form.selectbox(
							"boundaries",
							(
							"Red",
							"Blue (Lighter)"
							# ([66, 100, 200], [150, 180, 220]),
							# #Blue: dark and so light it gets mixed up with gray
							# ([100, 51, 112], [192, 190, 191]),
							# #Blue: dark and lighter but still blue
							# ([100, 51, 112], [183, 169, 154]),
							# ([25, 146, 190], [62, 174, 250]),
							# ([103, 86, 65], [145, 133, 128])
							)
								)
elif boundary_style == "Custom Boundaries":
	col1, col2 = form.columns(2)
	col1.header("Low Range")
	low_c1 = int(col1.text_input("Low Color 1", "0"))
	low_c2 = int(col1.text_input("Low Color 2", "0"))
	low_c3 = int(col1.text_input("Low Color 3", "255"))

	col2.header("High Range")
	high_c1 = int(col2.text_input("High Color 1", "255"))
	high_c2 = int(col2.text_input("High Color 2", "255"))
	high_c3 = int(col2.text_input("High Color 3", "255"))

	boundaries = [[low_c1, low_c2, low_c3], [high_c1, high_c2, high_c3]]

run_search = form.form_submit_button()
if run_search:
	if image_location == "IIIF":

		images = get_images(url)
	else:
		file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
		image = cv2.imdecode(file_bytes, 3)
		corrected_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		images = [image]
	col5, col6 = st.columns(2)
	for image in images:
		if image_location == 'IIIF':

			image = image.convert('RGB')

			image = np.array(image)


			col5.image(image)
		else:
			# pass
			# file_bytes = np.asarray(image, dtype=np.uint8)
			# image = cv2.imdecode(file_bytes, 3)
			# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			col5.image(corrected_image)
		dimensions = image.shape

		if boundaries == "Red":
			# Don't forget BGR
			boundaries = [[66, 100, 200], [150, 180, 220]]



		elif boundaries == "Blue (Lighter)":
			boundaries  = [[100, 51, 112], [192, 190, 191]]
		lower, upper = boundaries
		# lower, upper = boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype='uint8')

		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)
			# output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
		final = np.hstack([image, output])
		col6.image(mask)

		colored = cv2.countNonZero(mask)
		# col6.write(f"Number of Colored Pixles: {colored}")
		totalpixels = dimensions[0] * dimensions[1]
		# col6.write(f"Total Number of Pixles in Image: {totalpixels}")
		pixpercent = "{:.0%}".format(colored / totalpixels )
		# col6.write(f"Percentage of Pixles that Match {pixpercent}")
