import time
from setup import Get_data_site

results = Get_data_site() 
# time stamp 1 min , dane symulacyjne
dana_probna1 = 130.1 
dana_probna2 = 131.2
KROK = 128
PRZEKLADNIA = (80/30)
reference_point = 0 #polnoc jako punkt odniesienia od ktorego bedziemy obracac podstawe
MINUTE = 60


#Standardowy silnik NEMA23 wykonuje 200 pełnych kroków na 1 obrót- 1,8 stopnia. Po przełożeniu 80:30 wał wyjściowy potrzebuje 200 * 80 / 30 = 533.33 pełnych kroków na pełen obrót 360 stopni. Mozna robic mniejsze kroki 
def Pre_positioning():
    azimut = results[0][0]
    altidute = results[0][1]



    #zakladamy ze jest ustawiony na 1/32 kroku, kat bazowy 1,8 stopnia, 200 krokow - pelen obrot silnika ,  przelozenie 80/30 = 2,6667
    #200 * 32 * 80 / 30 = 17066,6667
    impuls_pre_positioning =int( azimut * ((200 * KROK * PRZEKLADNIA) /360))
    
    print(f"Liczba impulsow: {impuls_pre_positioning}")
def Pre_tracking():
    delta_azimut_per_second = ((results[1][0] - results[0][0]) / 60 ) #predkosc obrotu obiektu na niebie w stopniach na sekunde
    impuls_pre_tracking = ( delta_azimut_per_second * ((200 * KROK * PRZEKLADNIA) /360)) #to wylicza liczbe impulsow na sekunde (Hz)
    interval_seconds = 1.0 / impuls_pre_tracking #Co tyle ma wykonywac krok silnik
    next_step_time = time.perf_counter() #nie kumuluje bledu, oparte na zegarze systemowym
    print(f"predkosc obrotu obiektu na niebie: {delta_azimut_per_second}[deg/s],\nsilnik ma wykonywac krok co {interval_seconds} [s]. \n" )
    for seconds in range(MINUTE):
        while time.perf_counter() < next_step_time:
            time.sleep(0.0005)
        print("Obrot o krok ") #domyslnie tu bedzie stm32.move cczy cos
        next_step_time += interval_seconds

    





Pre_positioning()
Pre_tracking()