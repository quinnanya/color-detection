# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import streamlit as st
import pandas as pd
import numpy as np
import argparse
import cv2

st.title('Color detection')
# load the image

# define the list of boundaries
# Don't forget BGR
st.sidebar.header("Parameters")
form = st.sidebar.form("boundary form")
file = form.file_uploader('Upload a photo')
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
run_search = form.form_submit_button()
if run_search:
	file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
	image = cv2.imdecode(file_bytes, 1)
	st.image(image)
	dimensions = image.shape

	if boundaries == "Blue (Dark)":
		boundaries = [[[66, 100, 200], [150, 180, 220]]]
	elif boundaries == "Blue (Lighter)":
		boundaries  = [[[100, 51, 112], [192, 190, 191]]]
	# loop over the boundaries
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)

	colored = cv2.countNonZero(mask)
	st.write(colored)
	totalpixels = dimensions[0] * dimensions[1]
	st.write(totalpixels)
	pixpercent = "{:.0%}".format(colored / totalpixels )
	st.write(pixpercent)
	#	output = cv2.bitwise_and(image, image, mask = mask)

		# show the images
	#	cv2.imshow("images", np.hstack([image, output]))
	#	cv2.waitKey(0)
