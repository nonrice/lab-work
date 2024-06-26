'''
===============================================================================
Interactive	Image Segmentation using GrabCut algorithm.

This sample	shows interactive image	segmentation using grabcut algorithm.

USAGE:
	python grabcut.py <filename>

README FIRST:
	Two	windows	will show up, one for input	and	one	for	output.

	At first, in input window, draw	a rectangle	around the object using	the
right mouse	button.	Then press 'n' to segment the object (once or a	few	times)
For	any	finer touch-ups, you can press any of the keys below and draw lines	on
the	areas you want.	Then again press 'n' to	update the output.

Key	'0'	- To select	areas of sure background
Key	'1'	- To select	areas of sure foreground
Key	'2'	- To select	areas of probable background
Key	'3'	- To select	areas of probable foreground

Key	'n'	- To update	the	segmentation
Key	'r'	- To reset the setup
Key	's'	- To save the results
===============================================================================
'''

# Python 2/3 compatibility
from __future__	import print_function

import numpy as	np
import cv2 as cv
import argparse 

import sys, os

class App():
	BLUE = [255,0,0]		# rectangle	color
	RED	= [0,0,255]			# PR BG
	GREEN =	[0,255,0]		# PR FG
	BLACK =	[0,0,0]			# sure BG
	WHITE =	[255,255,255]	# sure FG

	DRAW_BG	= {'color' : BLACK,	'val' :	0}
	DRAW_FG	= {'color' : WHITE,	'val' :	1}
	DRAW_PR_BG = {'color' :	RED, 'val' : 2}
	DRAW_PR_FG = {'color' :	GREEN, 'val' : 3}

	# setting up flags
	rect = (0,0,1,1)
	drawing	= False			# flag for drawing curves
	rectangle =	False		# flag for drawing rect
	rect_over =	False		# flag to check	if rect	drawn
	rect_or_mask = 100		# flag for selecting rect or mask mode
	value =	DRAW_FG			# drawing initialized to FG
	thickness =	5			# brush	thickness
	
	mouse_prev = (-1, -1)

	def	onmouse(self, event, x,	y, flags, param):
		# Draw Rectangle
		if event ==	cv.EVENT_RBUTTONDOWN:
			self.rectangle = True
			self.ix, self.iy = x,y

		elif event == cv.EVENT_MOUSEMOVE:
			if self.rectangle == True:
				self.img = self.img2.copy()
				cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
				self.rect =	(min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
				self.rect_or_mask =	0

		elif event == cv.EVENT_RBUTTONUP:
			self.rectangle = False
			self.rect_over = True
			cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
			self.rect =	(min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
			self.rect_or_mask =	0
			print("Press N to iterate grabcut. Use 0, 1, 2, 3 to refine segmentation by drawing.")

		# draw touchup curves

		if event ==	cv.EVENT_LBUTTONDOWN:
			if self.rect_over:
				self.drawing = True
				cv.circle(self.img,	(x,y), self.thickness, self.value['color'],	-1)
				cv.circle(self.mask, (x,y),	self.thickness,	self.value['val'], -1)
				self.mouse_prev = (x, y)

		elif event == cv.EVENT_MOUSEMOVE:
			if self.drawing	== True:
				cv.line(self.img, (x, y), self.mouse_prev, self.value['color'], self.thickness)
				cv.line(self.mask, (x, y), self.mouse_prev, self.value['val'], self.thickness)
				self.mouse_prev = (x, y)

		elif event == cv.EVENT_LBUTTONUP:
			if self.drawing	== True:
				self.drawing = False
				cv.circle(self.img,	(x,	y),	self.thickness,	self.value['color'], -1)
				cv.circle(self.mask, (x, y), self.thickness, self.value['val'],	-1)

	def	run(self, in_path, out_path):
		self.img = cv.imread(in_path)
		
		self.img2 =	self.img.copy()								  #	a copy of original image
		self.mask =	np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
		self.output	= np.zeros(self.img.shape, np.uint8)		   # output	image to be	shown

		# input	and	output windows

		cv.namedWindow('output')
		cv.namedWindow('input')
		cv.setMouseCallback('input', self.onmouse)
		cv.moveWindow('input', self.img.shape[1]+10,90)
		cv.setWindowTitle('input', os.path.basename(in_path))
		cv.setWindowTitle('output', "Applied Mask Preview")

		print("Draw rectangle around subject using right mouse")

		while(1):
			cv.imshow('output', self.output)
			cv.imshow('input', self.img)
			k =	cv.waitKey(1)

			# key bindings
			if k ==	27:			# esc to exit
				break
			elif k == ord('0'):	# BG drawing
				print("Now marking background")
				self.value = self.DRAW_BG
			elif k == ord('1'):	# FG drawing
				print("Now marking foreground")
				self.value = self.DRAW_FG
			elif k == ord('2'):	# PR_BG	drawing
				print("Now marking probable background")
				self.value = self.DRAW_PR_BG
			elif k == ord('3'):	# PR_FG	drawing
				print("Now marking probable foreground")
				self.value = self.DRAW_PR_FG
			elif k == ord('s'):	# save image
				bar	= np.zeros((self.img.shape[0], 5, 3), np.uint8)
				res	= np.hstack((self.img2,	bar, self.img, bar,	self.output))
				print(out_path)
				cv.imwrite(out_path, np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8'))
				print("Saved mask")
			elif k == ord('r'):	# reset	everything
				self.rect =	(0,0,1,1)
				self.drawing = False
				self.rectangle = False
				self.rect_or_mask =	100
				self.rect_over = False
				self.value = self.DRAW_FG
				self.img = self.img2.copy()
				self.mask =	np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
				self.output	= np.zeros(self.img.shape, np.uint8)		   # output	image to be	shown
			elif k == ord('n'):	# segment the image
				try:
					bgdmodel = np.zeros((1,	65), np.float64)
					fgdmodel = np.zeros((1,	65), np.float64)
					if (self.rect_or_mask == 0):		 # grabcut with	rect
						cv.grabCut(self.img2, self.mask, self.rect,	bgdmodel, fgdmodel,	1, cv.GC_INIT_WITH_RECT)
						self.rect_or_mask =	1
					elif (self.rect_or_mask	== 1):		 # grabcut with	mask
						cv.grabCut(self.img2, self.mask, self.rect,	bgdmodel, fgdmodel,	1, cv.GC_INIT_WITH_MASK)
				except:
					import traceback
					traceback.print_exc()

			mask2 =	np.where((self.mask==1)	+ (self.mask==3), 255, 0).astype('uint8')
			self.output	= cv.bitwise_and(self.img2,	self.img2, mask=mask2)

		print('Done')


if __name__	== '__main__':
	parser = argparse.ArgumentParser(description='Process some images.')

	# Add the arguments
	parser.add_argument('--in', dest='in_path', required=True, help='Input file path')
	parser.add_argument('--out', dest='out_path', required=True, help='Output file path')
	parser.add_argument('--dir', action='store_true', help='Process directories')
	args = parser.parse_args()

	if args.dir:
		for root, dirs, files in os.walk(args.in_path):
			for file in files:
				if file.endswith('.jpg') or file.endswith('.png'):
					in_path = os.path.join(root, file)
					out_path = os.path.join(args.out_path, file)
					App().run(in_path, out_path)
					cv.destroyAllWindows()
	else:
		App().run(args.in_path, args.out_path)
		cv.destroyAllWindows()
