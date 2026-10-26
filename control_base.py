from data import Get_data_site

results = Get_data_site() 
# time stamp 1 min , dane symulacyjne
dana_probna1 = 130.1 
dana_probna2 = 131.2
krok = 32 
przekladnia = (80/30)
reference_point = 0 #polnoc jako punkt odniesienia od ktorego bedziemy obracac podstawe



#Standardowy silnik NEMA23 wykonuje 200 pełnych kroków na 1 obrót- 1,8 stopnia. Po przełożeniu 80:30 wał wyjściowy potrzebuje 200 * 80 / 30 = 533.33 pełnych kroków na pełen obrót 360 stopni. Mozna robic mniejsze kroki 
def Pre_positioning():
    azimut = results[0][0]
    altidute = results[0][1]



    #zakladamy ze jest ustawiony na 1/32 kroku, kat bazowy 1,8 stopnia, 200 krokow - pelen obrot silnika ,  przelozenie 80/30 = 2,6667
    #200 * 32 * 80 / 30 = 17066,6667
    impuls =int( azimut * ((200 * krok * przekladnia) /360))
    
    print(f"Liczba impulsow: {impuls}")

Pre_positioning()