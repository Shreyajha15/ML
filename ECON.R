library(foreign)
library(fBasics)
gun <- read.dta("guns.dta")

library(ggplot2)
library(ggcorrplot)

###Following is the code for the Exploratory Data Analysis which we have included in our project.
col <- colorRampPalette(c("#BB4444", "#EE9988", "#FFFFFF", "#77AADD", "#4477AA"))

ggcorrplot(cor(gun),hc.order = TRUE, type = 'lower', lab = TRUE)

###Plot of Stateid Vs Violence######
ggplot(gun,aes(stateid,vio)) + 
  geom_bar(stat = "identity",fill="black", na.rm=TRUE)

###Plot of Year Vs Violence######
ggplot(gun,aes(x = year, y = vio)) + 
  geom_bar(stat = "identity",fill="steelblue", na.rm=TRUE)

###Plot of Year Vs Murder######
ggplot(gun,aes(x = year, y = mur)) + 
  geom_bar(stat = "identity", fill = "green", na.rm = TRUE)

###Plot of Year Vs Population#####
ggplot(gun,aes(x = year, y = pop)) + 
  geom_bar(stat = "identity", fill = "red", na.rm = TRUE)

###Line Curve of Violence vs Year#####

ggplot(gun,aes(x=year,y=vio))+geom_smooth()

