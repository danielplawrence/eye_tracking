###########################################################################
#Example code for fixation analysis using the EyeTribe tracker and PyGaze
#This code is a bit of a mess! But it is designed to demonstrate how to 
#Extract and analyze gaze data from a visual world experiment written in Python
#The data are a set of time-stamped fixations and message logs
#First the fixation and message data are separated, then we tag the fixation data
#With information about each trial (i.e. which of four images was selected)
#The script then calls ggplot to show heatmap-type analyses of fixations and 
#Bar plots showing proportion of fixations on each area of interest.
#Happy tracking! Please get in touch if you are interested in developing/analyzing
#experiments with the EyeTribe tracker!
#Daniel Lawrence 04/02/2016
#s1122689@sms.ed.ac.uk
###########################################################################
library(scales)
data<-read.csv('/Users/pplsuser/Desktop/Eye_tracking/PyTribe/example/data/log.tsv',sep='\t',stringsAsFactors=F)
#These constants describe the screen size and top left-hand corners of the AOIs
dispsize=c(1280, 900)
tl=c(298, 165)
bl=c(298, 480)
tr=c(618, 165)
br =c(618, 480)
#Separate the header from the tracking data
trial_data<-data[!is.na(data$rawx),]
fix_data<-trial_data[data$timestamp!="MSG",]
fix_data<-trial_data[data$timestamp!="selected",]
fix_data<-fix_data[complete.cases(fix_data),]
fix_data$time<-as.numeric(fix_data$time)
#Extract the trial data and rename
trials<-trial_data[trial_data$timestamp=='MSG',c(2:5,7,9)]
names(trials)<-c('timestamp','time','state','trial','trialinfo','selected')
trials$time<-as.numeric(trials$time)
#Add a column to the tracking data for 'trial'
get_trial<-function(time){
	starts<-trials[trials$state=='start_trial'&trials$time<=time,]
	ends<-trials[trials$state=='end_trial'&trials$time>=time,]

	out<-starts[starts$trial %in% ends$trial,]$trial
	if (length(out)>0){
		return(out)
	} else{

		return('NA')
	}

}
fix_data$trial<-unlist(sapply(fix_data$time,get_trial))
#Add a column for the selected image
get_selected<-function(trial){
	if (trial!='NA'){
	selected<-trials[trials$trial==trial&trials$state=='end_trial',]$selected
	selected<-gsub("\\[|\\]", "", selected)
	selected<-gsub("[[:space:]]", "", selected)
	selected<-strsplit(selected,',')
	selected<-unlist(selected)
	aois<-c('tl','bl','tr','br')
	return(aois[which(selected=='True')])} else {
		return('NA')
	}
}
fix_data$selected<-unlist(sapply(fix_data$trial,get_selected))
#Function for coding fixations by ROI
get_aoi<-function(self.pos,self.size,posx,posy){
return((posx > self.pos[1] & posx < self.pos[1]+self.size) & (posy > self.pos[2] & posy < self.pos[2]+self.size))
}
which_aoi<-function(posx,posy){
bl=c(298, 165)
tl=c(298, 480)
br=c(618, 165)
tr =c(618, 480)
if (get_aoi(tl,300,posx,posy)==TRUE){return('TL')} else if (get_aoi(bl,300,posx,posy)==TRUE){
	return('BL')} else if (get_aoi(tr,300,posx,posy)==TRUE){
		return('TR')} else if (get_aoi(br,300,posx,posy)==TRUE){
			return('BR')} else {return('NA')}
}
fix_data$which_aoi<-mapply(which_aoi,posx=fix_data$rawx,fix_data$rawy)
#Plot ROIs & fixations
#Note that I think the y-axis needs to be flipped here!
#Hacked this by renaming the AOIs -- certainly needs checking in the future!
fix_data[fix_data$selected=='br',]$selected<-'tt'
fix_data[fix_data$selected=='tr',]$selected<-'br'
fix_data[fix_data$selected=='tt',]$selected<-'tr'
fix_data[fix_data$selected=='bl',]$selected<-'tt'
fix_data[fix_data$selected=='tl',]$selected<-'bl'
fix_data[fix_data$selected=='tt',]$selected<-'tl'
library(ggplot2)
fix_data<-fix_data[fix_data$selected!='NA',]
#Heatmap
ggplot(fix_data,aes(x=as.numeric(rawx),y=as.numeric(rawy),color=selected))+geom_point()+stat_density2d()+xlim(c(0,1280))+ylim(c(0,900))+geom_rect(xmin=tl[1],xmax=tl[1]+300,ymin=tl[2],ymax=tl[2]+300,fill=NA,color='black')+geom_rect(xmin=tr[1],xmax=tr[1]+300,ymin=tr[2],ymax=tr[2]+300,fill=NA,color='black')+geom_rect(xmin=bl[1],xmax=bl[1]+300,ymin=bl[2],ymax=bl[2]+300,fill=NA,color='black')+geom_rect(xmin=br[1],xmax=br[1]+300,ymin=br[2],ymax=br[2]+300,fill=NA,color='black')+facet_wrap(~trial)
#Proportion of fixations in each AOI
ggplot(fix_data,aes(x=which_aoi,y= (..count..)/ sapply(PANEL, FUN=function(x) sum(count[PANEL == x])),fill=selected))+geom_bar()+facet_wrap(~trial)+scale_y_continuous(labels = percent)+ylab('Proportion of fixations')+xlab('AOI')
ggplot(fix_data)