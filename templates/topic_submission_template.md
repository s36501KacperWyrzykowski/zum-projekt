# Zgłoszenie tematu

Odpowiedź mieści się na jednej stronie. Projekt dotyczy nadzorowanej klasyfikacji jednolabelowej: każdy przykład ma dokładnie jedną klasę.

1. Roboczy tytuł: **Klasyfikacja piłkarzy do jednego z przedziałów zarobków na podstawie ich statystyk i cech.**
2. Modalność (tekst, obraz, audio albo dane multimodalne): **Dane liczbowe z tabeli oraz tekstowy opis piłkarza (np. biografia).**
3. Problem klasyfikacji (co jest klasą i ile jest klas): **Klasą jest poziom rocznych zarobków piłkarza podzielony na przedziały: `Niski`, `Średni` oraz `Wysoki`.**
4. Pytanie eksperymentalne (co chcesz sprawdzić): **Czy na podstawie dostępnych danych model będzie w stanie przypisać nowego piłkarza do odpowiedniej klasy?**
5. Źródło danych (link): https://www.kaggle.com/datasets/ultimus/football-salaries-dataset 
6. Przybliżona wielkość zbioru: **4000 wierszy (zawodników) oraz 20 kolumn (cech zawodników) 16 liczbowe/ 4 opisowe.**
7. Lista klas i sposób oznaczenia etykiet:
 **`0` – `Niski`: zarobki poniżej 25-go percentyla w zbiorze (np. < 500k € / rok)**
 **`1` – `Średni`: zarobki pomiędzy 25-tym a 75-tym percentylem (np. 500k € – 3M € / rok)**
 **`2` – `Wysoki`: zarobki powyżej 75-go percentyla (np. > 3M € / rok)**
8. Licencja danych: **Public Domain / Open Data Common**
9. Proponowana jednostka generalizacji: **Jednostką generalizacji jest pojedynczy piłkarz.**
10. Planowany baseline: **Model oparty na podstawowych statystykach liczbowych (regresja logistyczna).**
11. Wstępny pomysł na model pretrained: **Użyję gotowego modelu językowego, żeby zebrał opisy zawodników i zamienił je na wektory.**
12. Potencjalne ograniczenia obliczeniowe: **Podejście czysto tabularne ma minimalne wymagania sprzętowe.**
13. Dane osobowe, wrażliwe albo z ograniczeniami dostępu lub redystrybucji: **Nie ma danych osobowych ani wrażliwych, wszystkie informacje są powszechnie dostępne.**
