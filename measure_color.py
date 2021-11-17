# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import streamlit as st
import pandas as pd
import numpy as np
import argparse
import cv2

st.title('Color Detection App')
st.sidebar.image('logo/stanford-logo.png')
# load the image

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
if boundary_style == "Standard Boundaries":
	boundaries = form.selectbox(
							"boundaries",
							(
							"Blue (Dark)",
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
	col5, col6 = st.columns(2)
	file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
	image = cv2.imdecode(file_bytes, 3)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	col5.image(image)
	dimensions = image.shape

	if boundaries == "Blue (Dark)":
		boundaries = [[[66, 100, 200], [150, 180, 220]]]
	elif boundaries == "Blue (Lighter)":
		boundaries  = [[[100, 51, 112], [192, 190, 191]]]
	else:
		boundaries = [boundaries]
	# loop over the boundaries
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)

	colored = cv2.countNonZero(mask)
	col6.write(f"Number of Colored Pixles: {colored}")
	totalpixels = dimensions[0] * dimensions[1]
	col6.write(f"Total Number of Pixles in Image: {totalpixels}")
	pixpercent = "{:.0%}".format(colored / totalpixels )
	col6.write(f"Percentage of Pixles that Match {pixpercent}")
	#	output = cv2.bitwise_and(image, image, mask = mask)

		# show the images
	#	cv2.imshow("images", np.hstack([image, output]))
	#	cv2.waitKey(0)
