##############################################################################
#Eye tracking with Python and the EyeTribe tracker
#Presented at Speerlab, The Ohio State University
#Daniel Lawrence, The University of Edinburgh
#s1122689@sms.ed.ac.uk
##############################################################################
#This code presents an example of an imagined eye-tracking experiment
#I have created it so that researchers who want to use the EyeTribe tracker
#have an idea of how they might program an experiment fairly easily
#The experiment concerns the process by which listeners intuit social traits
#from phonetic variation. 
##
#The design is based on the visual world paradigm -- listeners hear a set of 
#synthesised speech tokens and are asked to select the most appropriate
#character from a set of four. These characters vary in terms of their age,
#occupation and urban/rural origin. On each trial, listeners hear a speech
#token and select from four of the images (such that one social characteristic
#is held constant on a given trial). We are interested in whether images
#with certain characteristics are entertained as alternatives more strongly 
#than others prior to the final decision. For example, if a particular variant
#is associated with older, middle-class speakers in production, do we see
#high rates of fixation on a younger, middle-class competitor when choosing 
#from older/younger middle/working images.
##
#Clearly the premise for the experiment is pretty vague, but it allows me to
#provide examples of key elements of eye-tracking tasks e.g. audio/visual
#stimuli, data-logging.
##############################################################################
import os
import sys
import subprocess
import pygame
import numpy
import time
from random import shuffle
from constants import *
from pygaze import libtime
from pygaze.libtime import clock
from pygaze.libgazecon import AOI
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze.libinput import Mouse
from pygaze.eyetracker import EyeTracker
from pygaze import liblog
from psychopy import event
# # # # #
# SETUP

# visuals
disp = Display()
scr = Screen()
blnk= Screen()
#audio
pygame.mixer.init(frequency=44100,size=-16,buffer=2048,channels=1)
# input
mouse = Mouse(visible=True)
kb = Keyboard()

#Start tracker and calibrate
eyetracker = EyeTracker(disp)
eyetracker.calibrate()
#set up logging
log = liblog.Logfile()
#########################################################################
#Load image files
#image stimuli. 
image1 = {'number':0,'name':"images/M_Y_MC_L_1.png",'age':"Y",'gender':"M",'soc':"M",'loc':"L"}
image2 = {'number':1,'name':"images/M_O_MC_L_1.png",'age':"O",'gender':"M",'soc':"M",'loc':"L"}
image3 = {'number':2,'name':"images/M_Y_WC_L_1.png",'age':"Y",'gender':"M",'soc':"W",'loc':"L"}
image4 = {'number':3,'name':"images/M_O_WC_L_1.png",'age':"O",'gender':"M",'soc':"W",'loc':"L"}
image5 = {'number':4,'name':"images/M_Y_MC_NL_1.png",'age':"Y",'gender':"M",'soc':"M",'loc':"N"}
image6 = {'number':5,'name':"images/M_O_MC_NL_1.png",'age':"O",'gender':"M",'soc':"M",'loc':"N"}
image7 = {'number':6,'name':"images/M_Y_WC_NL_1.png",'age':"Y",'gender':"M",'soc':"W",'loc':"N"}
image8 = {'number':7,'name':"images/M_O_WC_NL_1.png",'age':"O",'gender':"M",'soc':"W",'loc':"N"}
#image files
IMGDIR = os.path.join(DIR, 'images')
imagefiles = [pygame.image.load(os.path.join(IMGDIR,"M_Y_MC_L_1.png")),
pygame.image.load(os.path.join(IMGDIR,"M_O_MC_L_1.png")),
pygame.image.load(os.path.join(IMGDIR,"M_Y_WC_L_1.png")),
pygame.image.load(os.path.join(IMGDIR,"M_O_WC_L_1.png")),
pygame.image.load(os.path.join(IMGDIR,"M_Y_MC_NL_1.png")),
pygame.image.load(os.path.join(IMGDIR,"M_O_MC_NL_1.png")),
pygame.image.load(os.path.join(IMGDIR,"M_Y_WC_NL_1.png")),
pygame.image.load(os.path.join(IMGDIR,"M_O_WC_NL_1.png"))]

images =[image1,image2,image3,image4,image5,image6,image7,image8]
#########################################################################
#Load sound files
#audio stimuli
sound1 = {'number':0,'name':'jb_day_dip.wav','speaker':"John",'word':"DAY",'vowel':"EY",'variant':"DIP"}
sound2= {'number':1,'name':'jb_day_mono.wav','speaker':"John",'word':"DAY",'vowel':"EY",'variant':"MONO"}
sound3 = {'number':2,'name':'jb_taste_dip.wav','speaker':"John",'word':"TASTE",'vowel':"EY",'variant':"DIP"}
sound4 = {'number':3,'name':'jb_taste_mono.wav','speaker':"John",'word':"TASTE",'vowel':"EY",'variant':"MONO"}
sound5 = {'number':4,'name':'jb_food_back_raised.wav','speaker':"John",'word':"FOOD",'vowel':"UW",'variant':"BACK"}
sound6 = {'number':5,'name':'jb_food_back_lowered.wav','speaker':"John",'word':"FOOD",'vowel':"UW",'variant':"BACK_LOW"}
sound7 = {'number':6,'name':'jb_food_mid_raised.wav','speaker':"John",'word':"FOOD",'vowel':"UW",'variant':"MID"}
sound8 = {'number':7,'name':'jb_food_mid_lowered.wav','speaker':"John",'word':"FOOD",'vowel':"UW",'variant':"MID_LOW"}
sound9 = {'number':8,'name':'jb_food_front_raised.wav','speaker':"John",'word':"FOOD",'vowel':"UW",'variant':"FRONT"}
sound10 = {'number':9,'name':'jb_food_front_lowered.wav','speaker':"John",'word':"FOOD",'vowel':"UW",'variant':"FRONT_LOW"}
sound11 = {'number':10,'name':'jb_two_back_raised.wav','speaker':"John",'word':"TWO",'vowel':"UW",'variant':"BACK"}
sound12 = {'number':11,'name':'jb_two_back_lowered.wav','speaker':"John",'word':"TWO",'vowel':"UW",'variant':"BACK_LOW"}
sound13 = {'number':12,'name':'jb_two_mid_raised.wav','speaker':"John",'word':"TWO",'vowel':"UW",'variant':"MID"}
sound14 = {'number':13,'name':'jb_two_mid_lowered.wav','speaker':"John",'word':"TWO",'vowel':"UW",'variant':"MID_LOW"}
sound15 = {'number':14,'name':'jb_two_front_raised.wav','speaker':"John",'word':"TWO",'vowel':"UW",'variant':"FRONT"}
sound16 = {'number':15,'name':'jb_two_front_lowered.wav','speaker':"John",'word':"TWO",'vowel':"UW",'variant':"FRONT_LOW"}
sound17 = {'number':16,'name':'jb_toast_back_dip.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"BACK_DIP"}
sound18 = {'number':17,'name':'jb_toast_mid_dip.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"MID_DIP"}
sound19 = {'number':18,'name':'jb_toast_front_dip.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"FRONT_DIP"}
sound20 = {'number':19,'name':'jb_toast_back_mono.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"BACK_MONO"}
sound21 = {'number':20,'name':'jb_toast_mid_mono.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"MID_MONO"}
sound22 = {'number':21,'name':'jb_toast_front_mono.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"FRONT_MONO"}
sound23 = {'number':22,'name':'jb_toast_mid_onset.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"MID_ONSET"}
sound24 = {'number':23,'name':'jb_toast_front_onset.wav','speaker':"John",'word':"TOAST",'vowel':"OW",'variant':"FRONT_ONSET"}
sound25 = {'number':24,'name':'jb_so_back_dip.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"BACK_DIP"}
sound26= {'number':25,'name':'jb_so_mid_dip.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"MID_DIP"}
sound27 = {'number':26,'name':'jb_so_front_dip.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"FRONT_DIP"}
sound28 = {'number':27,'name':'jb_so_back_mono.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"BACK_MONO"}
sound29 = {'number':28,'name':'jb_so_mid_mono.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"MID_MONO"}
sound30 = {'number':29,'name':'jb_so_front_mono.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"FRONT_MONO"}
sound31 = {'number':30,'name':'jb_so_mid_onset.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"MID_ONSET"}
sound32 = {'number':31,'name':'jb_so_front_onset.wav','speaker':"John",'word':"SO",'vowel':"OW",'variant':"FRONT_ONSET"}
#audio files
SNDDIR = os.path.join(DIR, 'audio')
sounds=[sound1,sound2,sound3,sound4,sound5,sound6,sound7,sound8,sound9,sound10,sound11,sound12,sound13,sound14,sound15,sound16,sound17,sound18,sound19,sound20,sound21,sound22,sound23,sound24,sound25,sound26,sound27,sound28,sound29,sound30,sound31,sound32]
#########################################################################
#Create trial objects
#These 'trial' objects are the image sets -- after creating these structures we assign them to sound samples

trial1= {'id':1,'images':[image2,image4,image6,image8],'constant':"age",'value':"O",'sound':"",'word':""};

trial2= {'id':2,'images':[image1,image3,image5,image7],'constant':"age",'value':"Y",'sound':"",'word':""};

trial3={'id':3,'images':[image3,image4,image7,image8],'constant':"soc",'value':"M",'sound':"",'word':""};

trial4={'id':4,'images':[image1,image2,image5,image6],'constant':"soc",'value':"W",'sound':"",'word':""};

trial5={'id':5,'images':[image1,image2,image3,image4],'constant':"loc",'value':"L",'sound':"",'word':""};

trial6={'id':6,'images':[image5,image6,image7,image8],'constant':"loc",'value':"N",'sound':"",'word':""};

trials=[trial1,trial2,trial3,trial4,trial5,trial6];

#This code creates the experimental items by looping through each sound and adding it to each image set
items=[]
for sound in sounds:
	for trial in trials:
		newtrial=trial.copy()
		newtrial['sound']=sound['number']
		newtrial['word']=sound['word']
		newtrial['file']=sound['name']
		items.append(newtrial)
#Simple randomization -- for a real experiment you would probably want to find a way to do non-consecutive 
#randomization
shuffle(items)
#########################################################################
#This code works out where to position the images and text
size=imagefiles[0].get_rect().size
centre=(0.5*DISPSIZE[0],0.5*DISPSIZE[1])
calibpoints1 = []
for x in [0.35,0.6]:
	for y in [0.35,0.7]:
		calibpoints1.append((int(x*DISPSIZE[0]),int(y*DISPSIZE[1])))
print(calibpoints1)
#These are AOI objects from the PyGaze package. They allow us to track click location easily.
#Notice the adjustment to the position (-150, -150) -- this is because AOIs are defined from the 
#top left-hand corner of the rectangle, unlike images which go from the center
tlAOI=AOI('rectangle',pos=tuple(map(sum,zip(calibpoints1[0],(-150,-150)))),size=size)
blAOI=AOI('rectangle',pos=tuple(map(sum,zip(calibpoints1[1],(-150,-150)))),size=size)
trAOI=AOI('rectangle',pos=tuple(map(sum,zip(calibpoints1[2],(-150,-150)))),size=size)
brAOI=AOI('rectangle',pos=tuple(map(sum,zip(calibpoints1[3],(-150,-150)))),size=size)
#This is a constant for setting the position of the text 
textpos=tuple(map(sum,zip(centre,(-36,+360))))
#########################################################################
#Here we have the 'body' of the experiment
#It simply loads the first trial, starts the eyetracker, and listeners for click events
#When it detects a click, it logs the trial info to the tracker log
#The tracker log will stream tracking info all the time, so it will be necessary to extract
#Chunks of tracking info between the 'start_trial' and 'end_trial' tags
#When all items have been presented, tracker recording is terminated.
def main():
	ntrial=0
	this=updateimages(ntrial)
	eyetracker.start_recording()
	#I'm going to log information about the position of everything to aid in the analysis
	eyetracker.log("dispsize" + "\t" + str(DISPSIZE))
	eyetracker.log("tl" + "\t" + str(tuple(map(sum,zip(calibpoints1[0],(-150,-150))))))
	eyetracker.log("bl" + "\t" + str(tuple(map(sum,zip(calibpoints1[1],(-150,-150))))))
	eyetracker.log("tr" + "\t" + str(tuple(map(sum,zip(calibpoints1[2],(-150,-150))))))
	eyetracker.log("br" + "\t" + str(tuple(map(sum,zip(calibpoints1[3],(-150,-150))))))
	sel='NA'
	eyetracker.log("start_trial" + "\t" + str(ntrial) + "\t" + "trialinfo" + "\t" +  str(this) + "\t" + "selected" + "\t" +  str(sel))
	while ntrial < len(items):
		clk=mouse.get_clicked()
		eyetracker.stop_recording()
		if clk[0]==1:
			sel=which_aoi(clk[1])
			print(str(this))
			eyetracker.log("end_trial" + "\t" + str(ntrial) + "\t" + "trialinfo" + "\t" +  str(this) + "\t" + "selected" + "\t" +  str(sel))
			ntrial=ntrial+1
			this=updateimages(ntrial)
			eyetracker.start_recording()
			sel='NA'
			eyetracker.log("start_trial" + "\t" + str(ntrial) + "\t" + "trialinfo" + "\t" +  str(this) + "\t" + "selected" + "\t" +  str(sel))
		if clk[0]==3:
			quit()
	if ntrial>len(items):
		eyetracker.stop_recording()
		eyetracker.close()
	
#########################################################################
def updateimages(count):
		thistrial=items[count].copy()
		scr.clear()
		scr.draw_fixation(fixtype='cross', colour=None, pw=1, diameter=12)
		#scr.draw_fixation(fixtype='cross', colour=None, pos=calibpoints1[2], pw=1, diameter=12)
		#scr.draw_fixation(fixtype='cross', colour=None, pos=calibpoints1[3], pw=1, diameter=12)
		#scr.draw_rect(colour=None, x=list(calibpoints1[0])[0]-150,y=list(calibpoints1[0])[1]-150,w=300,h=300)
		#scr.draw_rect( colour=None, x=list(calibpoints1[1])[0]-150,y=list(calibpoints1[1])[1]-150,w=300,h=300)
		#scr.draw_rect(colour=None, x=list(calibpoints1[2])[0]-150,y=list(calibpoints1[2])[1]-150,w=300,h=300)
		#scr.draw_rect( colour=None, x=list(calibpoints1[3])[0]-150,y=list(calibpoints1[3])[1]-150,w=300,h=300)
		disp.fill(scr)
		disp.show()
		time.sleep(2)
		im1=thistrial['images'][0]['name']
		im2=thistrial['images'][1]['name']
		im3=thistrial['images'][2]['name']
		im4=thistrial['images'][3]['name']
		scr.draw_image(im1,calibpoints1[0])
		scr.draw_image(im2,calibpoints1[1])
		scr.draw_image(im3,calibpoints1[2])
		scr.draw_image(im4,calibpoints1[3])
			#scr.draw_text(text='tl',pos=calibpoints1[0])
			#scr.draw_text(text='bl',pos=calibpoints1[1])
			#scr.draw_text(text='tr',pos=calibpoints1[2])
			#scr.draw_text(text='br',pos=calibpoints1[3])
		scr.draw_text(text=thistrial['word'],pos=textpos,fontsize=48)
		disp.fill(scr)
		t0=disp.show()
		soundname=thistrial['file']
		playsound(soundname)
		return(thistrial)
def playsound(name):
		file=os.path.join(SNDDIR,name)
		chana=pygame.mixer.Channel(1)
		chana.set_endevent()
		sounda=pygame.mixer.Sound(file)
		chana.play(sounda)
def which_aoi(pos):
	tl=tlAOI.contains(pos)
	tr=trAOI.contains(pos)
	bl=blAOI.contains(pos)
	br=brAOI.contains(pos)
	return[tl,bl,tr,br]

main()