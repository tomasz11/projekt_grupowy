import cv2
cap = cv2.VideoCapture("./data_base/planety_wszystkie.mp4")

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
        #cv2.putText(frame, "Saturn", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #tekst wiadomo
        cv2.putText(frame, f"{cord_centre_of_object}",(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #pokaz koordynaty srodka obiektu, przyda sie do algorytmu
    cv2.imshow("SkyWatcher", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()