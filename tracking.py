import cv2


cap = cv2.VideoCapture("./data_base/planety_wszystkie.mp4")
def Track_object():
    #pobranie szerokosci i wysokosci klatki nagrywanej przez kamere
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #format
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4',fourcc,20.0,(frame_width,frame_height))
    while cap.isOpened():
        ret,frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #konwertuj na skale szarosci
        blurred = cv2.GaussianBlur(gray, (5, 5), 0) # usuwa szumy z kosmosu (5,5) obszar jadra macierz pikseli ktora jest wyciagana srednia
        _, thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY) #zamiana obrazu na czarno bialy gdy jestmniejsze niz 40 staje sie czarne gdy wiecej to staje sie biale
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #funkcja szuka granicy miedzy przejsciem z bialego na czarne czyli konturu
        if contours:
            c = max(contours, key=cv2.contourArea) #wez pod uwage tylko najwiekszy kontur
            x, y, w, h = cv2.boundingRect(c) #pobierz wymiary prostokata w ktorym miesci sie obiekt
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #narysuj go na obrazie
            cord_centre_of_object = [(x+x+w)/2 , (y+y+h)/2] #koordynaty srodka obiektu
            cv2.putText(frame, f"{cord_centre_of_object}",(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #pokaz koordynaty srodka obiektu, przyda sie do algorytmu
        out.write(frame)
        cv2.imshow("SkyWatcher", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
Track_object()
    


    
    














"""
bedzie funkcja ktora ocenia ostrosc obrazu i wprowadza korekty, funkcja bedzie wykonywana podczas wykonywania funkcji Track_objeckt, moze da sie ja 
puscic w osobnym watku aby caly czas lekko korektowala ? nwm 

Gdy dana klatka obrazu bedzie ostrzejsza od poprzedniej, algorytm musi zapamietac pozycje pokretla , lecz probowac zdobyc jeszcze lepszy obraz jesli przekrecenie pogorszy
wraca do najlepszej opcji z przeszlosci

czy jest potrzebny algorytm dodatkowy po wtepnej korekcji obrazu ? 
czy da sie to zrobic inaczej niz metoda ogolna?
czy wyciaganie widma analiza itp cos zmieni?

"""