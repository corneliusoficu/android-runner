library(tidyverse)
#read data
wifi_data<-read_csv("Aggregated_Reps_Wifi.csv")
#summary the data
summary(wifi_data)
#check if the column data is numeric
unlist(lapply(wifi_data, is.numeric))
#get the numeric columns
num_cols<-colnames(wifi_data)[unlist(lapply(wifi_data, is.numeric))]
#get the distribution plots of all numeric columns
par(mfrow=c(3,4))
mapply(hist,wifi_data[num_cols],main=paste('Distribution of',num_cols),xlab=num_cols)
#the distribution plots of log,sqrt and reciprocal of batterystats_Joule_calculated
#(can change to other columns)
wifi_data<-wifi_data %>%
  mutate(batterystats_Joule_calculated_log = log(batterystats_Joule_calculated),
         batterystats_Joule_calculated_sqrt = sqrt(batterystats_Joule_calculated),
         batterystats_Joule_calculated_reciprocal = 1/batterystats_Joule_calculated)

wifi_data
plot_cols<-c('batterystats_Joule_calculated','batterystats_Joule_calculated_log',
             'batterystats_Joule_calculated_sqrt','batterystats_Joule_calculated_reciprocal')

mapply(hist,wifi_data[plot_cols],main=paste('Distribution of',plot_cols),xlab=plot_cols)
#check normality of batterystats_Joule_calculated and log
check_normality<-function(data){
  plot(density(data))
  qqnorm(data)
  car::qqPlot(data)
  #qqline(data, col=2, lwd=2)
  shapiro.test(data)
}

wifi_data$batterystats_Joule_calculated %>%
  check_normality

wifi_data$batterystats_Joule_calculated_log %>%
  check_normality()
