# KOKOS
 Koleżeńska Ochrona Kierowców Oraz Samochodów
## Cel i Opis
Aplikacja umożliwia użytkownikom łatwe i szybkie komunikowanie się z właścicielami samochodów w przypadku, gdy zauważą jakieś problemy związane z danym pojazdem. Użytkownicy mogą zeskanować kod QR umieszczony na szybie samochodu lub wprowadzić numer rejestracyjny, aby zidentyfikować właściciela i skontaktować się z nim za pośrednictwem aplikacji. Właścicielom umożliwia to szybką reakcję w przypadku potrzeby naprawy lub interwencji.
## Funkcjonalności
Możlwości aplikacji:
- tworzenie konta, dodawanie własnych rejestracji,
- identyfikacja właściciela pojazdu za pomocą kodu QR lub rejestracji,
- możliwość nawiązania konwersacji z nadawcą wiadomości,
- możliwość modyfikowania swojego konta,
- możliwość otrzymywania powiadomień mailowych,
  
## Struktura projektu
Projekt został podzielony na 3 foldery. 

<b>GUI</b> zawiera elementy interfejsu użytkownika dla czatu oraz uniwersalne dla aplikacji.

<b>data</b> Zawiera między innymi klasy odpowiedzialne za komunikację z bazą danych. Klasa AuthService związana jest z autoryzacją użytkownika, a DataProvider umożliwia uzyskiwanie danych o użytkownikach.

<b>screens</b> zawiera wszystkie widoki aplikacji wraz z ich warstwą graficzną. 
Aplikacja zawiera następujące widoki (wraz z ich odpowiedzialnością):
- adddamage - dodawanie nowej infrmacji dla właściciela pojazdu po zeskanowaniu kodu QR lub wpisaniu rejestracji
- addregistration - dodawanie rejestracji pojazdu
- chat - wyświetlanie konwersacji z innymi użytkownikami
- deletregistration - usuwanie rejestracji
- forgotpassword - resetowanie hasła
- login - logowanie użytkownika
- main - strona główna
- qr - wyszukiwanie użytkownika po kodzie QR
- registration - wyszukiwanie użytkownika po rejestracji
- settings - ustawienia konta
- signup - rejestracja użytkownika
- updateusername - zmiana nazwy użytkownika
- yourcode - wyświetlanie własnego kodu QR


Dodatkowo poza folderami jest plik app.py który pozwala na uruchomienie aplikacji.

## Technologie
Python 3.10

Kivy

Firebase

## Twórcy

Laura Wiktor

Sebastian Soczawa
