# Zgłoszenie tematu

Odpowiedź mieści się na jednej stronie. Projekt dotyczy nadzorowanej klasyfikacji jednolabelowej: każdy przykład ma dokładnie jedną klasę.

1. Roboczy tytuł: **Klasyfikacja piłkarzy do jednego z przedziałów zarobków na podstawie ich statystyk i cech.**
2. Modalność (tekst, obraz, audio albo dane multimodalne): **Dane multimodalne: liczbowe statystyki boiskowe piłkarza połączone z realnymi tekstowymi opisami i atrybutami profilowymi zawodnika (np. cechy gracza – player_traits, pozycje i style gry).**
3. Problem klasyfikacji (co jest klasą i ile jest klas): **Klasą jest poziom rocznych zarobków piłkarza podzielony na przedziały: `Niski`, `Średni` oraz `Wysoki`.**
4. Pytanie eksperymentalne (co chcesz sprawdzić): **Czy dodanie tekstowych reprezentacji z gotowego modelu pretrained (np. distilbert-base-multilingual-cased) do klasycznych statystyk liczbowych poprawi skuteczność klasyfikacji (mierzoną metryką Macro-F1) w porównaniu do klasycznego baseline'u (regresji logistycznej) na nowych, nieznanych zawodnikach?**
5. Źródło danych (link): https://www.kaggle.com/datasets/stefanoleone992/ea-sports-fc-24-complete-player-dataset
6. Przybliżona wielkość zbioru: **Około 19,000 wierszy (zawodników) oraz ponad 100 kolumn, zawierających statystyki liczbowe, cechy fizyczne oraz kolumny tekstowe (np. player_traits, player_positions), po uprzednim wykluczeniu cech bezpośrednio ujawniających zarobki lub wartość rynkową (takich jak value_eur czy release_clause_eur).**
7. Lista klas i sposób oznaczenia etykiet:
 **`0` – `Niski`: zarobki poniżej 25-go percentyla w zbiorze (np. < 500k € / rok)**
 **`1` – `Średni`: zarobki pomiędzy 25-tym a 75-tym percentylem (np. 500k € – 3M € / rok)**
 **`2` – `Wysoki`: zarobki powyżej 75-go percentyla (np. > 3M € / rok)**
8. Licencja danych: **Public Domain / Open Data Common**
9. Proponowana jednostka generalizacji: **Jednostką generalizacji jest pojedynczy piłkarz.**
10. Planowany baseline: **Model oparty na podstawowych statystykach liczbowych (regresja logistyczna).**
11. Wstępny pomysł na model pretrained: **Użycie zamrożonego encodera tekstowego (np. wielojęzycznego modelu distilbert-base-multilingual-cased z biblioteki Hugging Face) do przekształcenia tekstowych opisów atrybutów i profili zawodników na wektory reprezentacji (embeddings), które zostaną połączone z wektorem cech liczbowych w modelu docelowym.**
12. Potencjalne ograniczenia obliczeniowe: **Podejście czysto tabularne ma minimalne wymagania sprzętowe, a ekstrakcje wektorów z lekkiego modelu językowego mieszczą się w darmowych zasobach obliczeniowych (Google Colab / Kaggle Notebooks)**
13. Dane osobowe, wrażliwe albo z ograniczeniami dostępu lub redystrybucji: **Zbiór zawiera ogólnodostępne statystyki sportowe i szacunkowe zarobki osób publicznych (sportowców), bez wrażliwych danych osobowych (PII). Dane nie będą redystrybuowane w surowej formie w publicznym repozytorium (zgodnie z zasadami projektu zamieszczona zostanie tylko instrukcja pobrania i próbka).**
