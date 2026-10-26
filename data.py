import requests , re
from datetime import datetime, date,timezone,timedelta

def Setup():
    start_time = datetime.now(timezone.utc).replace(tzinfo=None) #utc zone !!!
    stop_time = start_time + timedelta(minutes = 1)         
    start_time_str = f"'{start_time}'"
    stop_time_str = f"'{stop_time}'"
    return start_time_str,stop_time_str

def Get_data_from_user():
    planety = {
        "1": "'199'",  # Merkury
        "2": "'299'",  # Wenus
        "3": "'499'",  # Mars
        "4": "'599'",  # Jowisz
        "5": "'699'",  # Saturn
        "6": "'799'",  # Uran
        "7": "'899'",  # Neptun
        "8": "'301'",  # Księżyc
    } 
    x = input(
        "Podaj numer planety : \n 1: Merkury \n 2: Wenus \n 3: Mars \n 4:"
        " Jowisz \n 5: Saturn \n 6: Uran \n 7: Neptun \n 8: Księżyc \nWybór: "
    ).strip()
    return planety.get(x,"'699'")


def Get_data_site():
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    # Parametry zapytania
    start_time,stop_time = Setup()
    planeta = Get_data_from_user()
    params = {
        "format": "json",                  
        "COMMAND": planeta,               # Co obserwuje w NASA ID
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER",
        "CENTER": "'coord@399'",           # Obserwator na powierzchni Ziemi
        "COORD_TYPE": "GEODETIC",
        "SITE_COORD": "'18.56269,54.41344,0.01'", # Polozenie geograficzne, Gdansk Oliwa : szerolkosc,dlugosc , przewyzszenie w km
        "START_TIME": start_time,        #utc jest wiec pokazuje o 2 h do tylu ale to nie ma znaczenia wyswietlac mozna na naszym timezone
        "STOP_TIME": stop_time,
        "STEP_SIZE": "'1m'",               # krok czasowy 1 minuta
        "QUANTITIES": "'4'"              
    }
    response = requests.get(url, params=params)
    data = response.json()
    raw_text = data["result"]
    result=[] 
    #print(data)
    #pobieram dane ktore mnie interesuja, wydzielam sekcje od SOE do EOE
    ephemeris_section = raw_text.split("$$SOE")[1].split("$$EOE")[0]
    important_lines = [line.strip() for line in ephemeris_section.strip().split("\n")]
    for line in important_lines:
        parts = line.split()
        date_str = parts[0]
        time_str = parts[1]

        # wszystkie liczby z wiersza sa zbierane, pomijam wszystkie znaczniki jakie moga sie pojawic 
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)

        # bierzemy zawsze dwie ostatnie liczby
        deg_az = float(numbers[-2])
        deg_alt = float(numbers[-1])

        print(
            f"DATE: {date_str}, TIME: {time_str}, AZ: {deg_az}, ALT: {deg_alt}"
        )
        result.append((deg_az, deg_alt))
    return result

