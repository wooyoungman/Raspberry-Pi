from calendar import calendar
from pyowm.owm import OWM
import pifacecad
import pygame
import time
import pytz
import sys
from pifacecad.tools.scanf import LCDScanf
from datetime import datetime

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

state=0
default=0
wait=1
set_Alarm=2
show_Alarm=3
end_pg=4
weather=5
pm_check=0
cptime=0
svtime=0
arr_num=0
set_ok=0
weather_check=0
weather_out=0
flag1=0
alr_flag=0
time_h_m=1
utc=pytz.utc
cad=pifacecad.PiFaceCAD()
listener = pifacecad.SwitchEventListener(chip=cad)
mykey='c62e681083cbe7b38584499ffbdc3437'
owm=OWM(mykey)
mgr=owm.weather_manager()

cad.lcd.backlight_on()

observation1=mgr.weather_at_place('Incheon,KR')
observation2=mgr.weather_at_place('Osaka,JP')
observation3=mgr.weather_at_place('Bangkok,TH')
observation4=mgr.weather_at_place('Paris,FR')
observation5=mgr.weather_at_place('New York,US')
observation6=mgr.weather_at_place('Tehran,IR')

weather1=observation1.weather
weather2=observation2.weather
weather3=observation3.weather
weather4=observation4.weather
weather5=observation5.weather
weather6=observation6.weather
city_name=['Incheon','Osaka','Bankok','Pairs','New York','Tehran']
city_weather=[weather1,weather2,weather3,weather4,weather5,weather6]

def move_left(event):
	global arr_num
	global city_name
	arr_num=arr_num-1
	#event.chip.lcd.set_cursor(0,1)
	#event.chip.lcd.write(city_name[arr_num])
	cad.lcd.clear()
	cad.lcd.set_cursor(0,0)
	cad.lcd.write('Which City?')
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(f'{city_name[arr_num]}')
	#print(f'{city_name[arr_num]}')
def move_right(event):
	global arr_num
	global city_name
	if arr_num<5:
		arr_num=arr_num+1
	#event.chip.lcd.set_cursor(0,1)
	#event.chip.lcd.write(city_name[arr_num])
	cad.lcd.clear()
	cad.lcd.set_cursor(0,0)
	cad.lcd.write('Which City?')
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(f'{city_name[arr_num]}')
def select_show(event):
	event.chip.lcd.clear()
	event.chip.lcd.write(f'{city_weather[arr_num].detailed_status}')
	time.sleep(0.5)
	cad.lcd.clear()
	global weather_out
	weather_out=1




#버튼 입력
def button_(event):
	global state
	state=event.pin_num

#리모컨 입력
def button_ir(event):
	global state
	state=int (event.ir_code)


#현재 시간
def Clock():
	now=datetime.utcnow().replace(tzinfo=utc)
	tz=pytz.timezone("Asia/Seoul")
	localr=tz.normalize(now.astimezone(tz))
	cad.lcd.set_cursor(0,0)
	cad.lcd.write("Seoul      ")
	cad.lcd.set_cursor(0,1)
	nt=localr.strftime("Now : %H:%M:%S")
	global cptime
	cptime=localr.strftime("%H%M")
	#print(cptime)
	cad.lcd.write(nt)
	#print(localr)
	time.sleep(0.6)

#알람 설정
def Alarm_set():
	global scanner
	global time1
	global save_time
	global time_h_m
	global flag1
	flag1=1
	cad.lcd.clear()
	cad.lcd.backlight_on()
	scanner=LCDScanf("Alarm %2i:%2i %m%r",custom_values=('AM','PM'))
	time1 = scanner.scan()
	if time1[2]=='PM':
		time1[0]+=12
	time_h_m=[f'{time1[0]:02d}{time1[1]:02d}']
	global set_ok
	set_ok=1
	#pygame.mixer.init()
	#pygame.mixer.music.set_volume(0.8)
	#sound=pygame.mixer.Sound("/home/pi/Alarm.wav")
	#sound.play(3)
	cad.lcd.clear()
	cad.lcd.set_cursor(0,0)
	cad.lcd.write("Alarm set")
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(f'at{time1[0]:02d}:{time1[1]:02d}{time1[2]}')
	time.sleep(1)
	cad.lcd.clear()
	global state
	state=wait

#알람 시간 보여주기
def Alarm_time_show():
	global time1
	cad.lcd.clear()
	cad.lcd.backlight_on()
	cad.lcd.set_cursor(0,0)
	cad.lcd.write("You set Alarm at : ")
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(f'{time1[0]:02d}:{time1[1]:02d}{time1[2]}')
	#print(time1[0],time1[1],time1[2])
	time.sleep(2)
	cad.lcd.clear()
	global state
	state=wait

#알람 울리기
def Alarm_on():
	global save_time
	global time1
	global time_h_m
	global pm_check
	global set_ok
	global state
	now=datetime.utcnow().replace(tzinfo=utc)
	tz=pytz.timezone("Asia/Seoul")
	localr=tz.normalize(now.astimezone(tz))
	#print(time1[0])
	nt1=localr.strftime('%H')
	nt2=localr.strftime('%M')
	nt3=nt1+nt2
	#print(nt3)
	save_time="".join(map(str,time_h_m))
	#print(save_time)
	if nt3==save_time :
		#print("RingRing")
		pygame.mixer.init()
		pygame.mixer.music.set_volume(0.5)
		sound=pygame.mixer.Sound("Alarm.wav")
		cad.lcd.clear()
		cad.lcd.set_cursor(0,0)
		cad.lcd.write("Wake up!")
		sound.play()
		set_ok=0
		while pygame.mixer.music.get_busy()==True:
			continue
		state=wait

#날씨 보여주기
def weather_show():
	cad.lcd.clear()
	global weather_check
	global weather_out
	global arr_num
	global city_name
	global city_weather
	global scanner
	global city
	global find_num
	find_num=0
	weather_check=1
	scanner=LCDScanf("Where? %m%r",custom_values=('Incheon','Osaka',
	'Bangkok','New York','Paris','Tehran'))
	city=scanner.scan()
	#print(city)
	for i in range(6):
		if city[0]==city_name[i]:
			find_num=i
	cad.lcd.clear()
	cad.lcd.write(city[0])
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(city_weather[find_num].detailed_status)
	time.sleep(1)
	cad.lcd.clear()
	#print(weather_check)
	global state
	state=1



listener.register(0,pifacecad.IODIR_FALLING_EDGE,button_) # 0번 버튼
listener.register(2,pifacecad.IODIR_FALLING_EDGE,button_) # 2번 버튼
listener.register(3,pifacecad.IODIR_FALLING_EDGE,button_) # 3번 버튼
listener.register(4,pifacecad.IODIR_FALLING_EDGE,button_) # 4번 버튼
listener.register(5,pifacecad.IODIR_FALLING_EDGE,button_) # 5번 버튼

irlistener = pifacecad.IREventListener(prog="myprogram",lircrc="/home/pi/.lircrc")
irlistener.register(str(0),button_ir)
irlistener.register(str(2),button_ir)
irlistener.register(str(3),button_ir)
irlistener.register(str(4),button_ir)
irlistener.register(str(5),button_ir)
irlistener.activate()

listener.activate()
while 1:
	#print(state)
	#print(cptime)
	#print(time_h_m)
	if set_ok==1 :
		if cptime=="".join(map(str,time_h_m)):
			Alarm_on()
	if state==default:
		Clock()
	elif state==wait:
		continue
	elif state==set_Alarm:
		Alarm_set()
	elif state==show_Alarm:
		Alarm_time_show()
	elif state==end_pg:
		cad.lcd.clear()
		cad.lcd.write("Program is end")
		sys.exit("Program is end")
	elif state==weather:
		weather_show()
	


	

	
