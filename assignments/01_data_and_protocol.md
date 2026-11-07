# Zadanie 1. Problem, dane i protokół eksperymentu

**Termin:** niedziela 8 listopada 2026, 23:59
**Punkty:** 15

## Cel

Zanim cokolwiek wytrenujesz, ustalasz, co mierzysz i jak, a final test zamrażasz.

## Wymagania

1. Problem klasyfikacji i pytanie eksperymentalne.
   * Problem polega na klasyfikacji piłkarzy do 3 przedziałów zarobków (`Niski`, `Średni`, `Wysoki`).
   * Pytanie eksperymentalne: Czy dodanie tekstowych reprezentacji z modelu pretrained do klasycznych statystyk liczbowych poprawi skuteczność klasyfikacji **(Macro-F1)** na nowych, nieznanych zawodnikach?
2. Jednostka generalizacji z uzasadnieniem: do jakich przyszłych danych ma działać model.
   * Jednostką generalizacji jest pojedynczy piłkarz. Model ma działać dla zawodników z nowych klubów/lig, których algorytm wcześniej nie widział, co sprawdzimy dzieląc dane na poziomie klubów.
3. Audyt danych:
 *  liczba przykładów i rozkład klas:
     W zbiorze znajduje się 18350 unikalnych piłkarzy z edycji FC 24. Rozkład klas na zbiorze treningowym wynosi odpowiednio: ok. 25% (Niski), 50% (Średni), 25% (Wysoki).
 *  braki danych:
      Rekordy z brakami w kluczowych zmiennych (`club_name` lub `wage_eur`) zostały odfiltrowane.
      W kolumnie `player_traits` braki oznaczają, że zawodnik nie ma przypisanych specjalnych cech i zostały zastąpione pustym ciągiem znaków*
 *  duplikaty (co najmniej dokładne, a jeśli to możliwe, także bardzo podobne): Zostało dodane sprawdzanie duplikatów po kolumnie (*player_id*)., ale nie występują.
  *  podstawowe statystyki wejścia (długość tekstu, rozmiar obrazu, czas trwania nagrania):
Kolumna 'player_traits': średnia długość = 8.9 znaków, max = 91 znaków
Kolumna 'player_positions': średnia długość = 5.1 znaków, max = 13 znaków
  *    kilka przykładów:
     short_name  overall  wage_eur player_positions                                                                      player_traits
0     K. Mbappé       91  230000.0           ST, LW                                                Quick Step +, Rapid, Flair, Trivela
1    E. Haaland       91  340000.0               ST                                              Acrobatic +, Power Header, Quick Step
2  K. De Bruyne       91  350000.0          CM, CAM    Pinged Pass +, Dead Ball, Incisive Pass, Long Ball Pass, Whipped Cross, Trivela
3      L. Messi       90   23000.0          CF, CAM  Technical +, Finesse Shot, Dead Ball, Pinged Pass, Tiki Taka, Quick Step, Trivela
4. Liczba niezależnych jednostek generalizacji w train, validation i final test, obok liczby przykładów. Na przykład 8000 nagrań może pochodzić tylko od 24 mówców. Wtedy podajesz zarówno liczbę nagrań, jak i liczbę mówców w każdym zbiorze. Jeżeli liczba niezależnych jednostek w validation albo final test jest mała, skomentuj, jak może to wpływać na stabilność estymaty. *
Zbiór Train:
  - Liczba przykładów (piłkarzy): 10974
  - Liczba niezależnych jednostek (klubów): 402
Zbiór Validation:
  - Liczba przykładów (piłkarzy): 3591
  - Liczba niezależnych jednostek (klubów): 134
Zbiór Final Test:
  - Liczba przykładów (piłkarzy): 3698
  - Liczba niezależnych jednostek (klubów): 134*
5. Potencjalne źródła wycieku danych w Twoim zbiorze i sposób, w jaki im zapobiegasz. Typowe źródła to te same osoby, nagrania, dokumenty albo źródła po obu stronach podziału, duplikaty, augmentacje i zależności czasowe.
* **1. Wyciek na poziomie jednostki generalizacji (wspólne kluby po obu stronach podziału):**
  * *Zagrożenie:* Zawodnicy grający w tym samym klubie charakteryzują się często podobną strukturą zarobków wynikającą z polityki finansowej drużyny. Gdyby zawodnicy z tego samego klubu trafili zarówno do zbioru treningowego (Train), jak i testowego, model mógłby „nauczyć się” specyfiki klubu zamiast uogólniać cechy zawodnika.
  * *Zabezpieczenie:* Zastosowano **podział grupowy (`GroupShuffleSplit`) na poziomie nazwy klubu (`club_name`)**. Dzięki temu kluby w zbiorach Train, Validation i Final Test są całkowicie rozłączne (co potwierdził automatyczny audyt wykazujący 0 wspólnych klubów między podziałami).
* **2. Wyciek poprzez cechy finansowe (Leakage Features):**
  * *Zagrożenie:* Kolumny takie jak rynkowa wartość zawodnika (`value_eur`) czy klauzula odstępnego (`release_clause_eur`) są niemal bezpośrednio matematycznie lub rynkowo powiązane z rocznym wynagrodzeniem (`wage_eur`). Ich obecność w cechach wejściowych doprowadziłaby do natychmiastowego „oszukania” modelu.
  * *Zabezpieczenie:* Cechy te zostały **całkowicie usunięte** ze zbioru danych przed rozpoczęciem jakichkolwiek eksperymentów modelowych.
* **3. Wyciek poprzez wyznaczanie progów klasowych:**
  * *Zagrożenie:* Obliczenie progów percentylowych (25% i 75%) dla podziału zarobków na całym zbiorze danych uwzględniałoby informacje z przyszłości (ze zbioru testowego).
  * *Zabezpieczenie:* Progi percentylowe definiujące klasy (`Niski`, `Średni`, `Wysoki`) wyznaczono **wyłącznie na zbiorze treningowym**, a następnie zastosowano je bez żadnych modyfikacji do zbiorów walidacyjnego i testowego.
* **4. Duplikaty i powtórzenia:**
  * *Zagrożenie:* Obecność tego samego piłkarza w różnych wariantach w bazie danych mogłaby spowodować, że duplikat trafi do treningu, a inny do testu.
  * *Zabezpieczenie:* Wykonano wstępne czyszczenie danych, usuwając duplikaty na podstawie unikalnego identyfikatora zawodnika (`player_id`).
6. Podział train, validation i final test zgodny z jednostką generalizacji: grupowy, stratyfikowany, czasowy albo oficjalny, z uzasadnieniem.
* **Typ podziału:** Grupowa walidacja krzyżowa / podział grupowy (*Group Shuffle Split*) połączony z podziałem hierarchicznym.
* **Uzasadnienie wyboru metody:** 
  - Wybrano **podział grupowy** z uwagi na zdefiniowaną jednostkę generalizacji, którą jest pojedynczy piłkarz w kontekście jego przynależności klubowej (`club_name`). 
  - W tradycyjnym podziale losowym zawodnicy z tego samego klubu mogliby trafić zarówno do zbioru treningowego, jak i testowego, co prowadziłoby do wycieku danych (kluby mają wspólną specyfikę finansową i treningową). Podział grupowy gwarantuje, że całe kluby wraz ze wszystkimi swoimi zawodnikami trafiają albo wyłącznie do zbioru treningowego, albo wyłącznie do walidacyjnego, albo do zamrożonego testu ostatecznego.
  - Zastosowano proporcje podziału wynoszące w przybliżeniu: **60% Train, 20% Validation oraz 20% Final Test**, zrealizowane dwuetapowo za pomocą biblioteki `scikit-learn` (`GroupShuffleSplit`), co zapewniło stabilność liczności próbek oraz pełną rozłączność klubową, co zostało zweryfikowane automatycznym skryptem audytowym.
7. Metryka główna i pomocnicze, z uzasadnieniem (na przykład macro F1 przy nierównych klasach).
* **Metryka główna: Macro-F1**
  * *Uzasadnienie:* Problem klasyfikacji zarobków jest wieloklasowy (3 klasy: Niski, Średni, Wysoki), a rozkład klas wykazuje naturalną nierównowagę (klasa średnia liczy ok. 50% przykładów, natomiast klasy skrajne po ok. 25%). Metryka **Macro-F1** oblicza średnią arytmetyczną miary F1 dla każdej klasy niezależnie, dzięki czemu traktuje każdą klasę z równą wagą. Zapobiega to sytuacji, w której model faworyzowałby najliczniejszą klasę średnią kosztem dokładności w klasach skrajnych.
* **Metryka pomocnicza: Accuracy (Dokładność) oraz Precision / Recall per klasa**
  * *Uzasadnienie:* Umożliwiają bieżącą weryfikację ogólnego odsetka poprawnych trafień oraz szczegółową analizę błędów popełnianych przez model w podziale na poszczególne przedziały zarobkowe.
8. Seed i zasady losowości.
* Wartość seed: `random_state = 42`
  Zastosowanie: Ustawione we wszystkich funkcjach losujących i podziałowych (np. `GroupShuffleSplit`). Zapewnia to pełną reprodukowalność eksperymentu oraz identyczne wyniki podziału danych przy każdym uruchomieniu skryptu.*
9. Licencja i podstawowa dokumentacja danych: skąd pochodzą, jak oznaczono klasy, znane ograniczenia.
* Źródło: EA Sports FC 24 complete player dataset (zbiór publiczny z platformy Kaggle / bazujący na danych SoFIFA).
  Licencja: CC0: Public Domain / Open Data Commons.
  Oznaczenie klas:** Klasy zarobkowe (`Niski`, `Średni`, `Wysoki`) wyznaczono automatycznie na podstawie 25. i 75. percentylu rocznych zarobków (`wage_eur`) wyliczonych wyłącznie na zbiorze treningowym.*
10. Zamrożenie final test. Identyfikatory przykładów każdego zbioru zapisujesz w `splits/` ([opis formatu](../splits/README.md)), robisz commit i tworzysz tag `task-1`. Od tej chwili nie uruchamiasz na final test żadnego modelu. Jeśli później musisz poprawić podział, stosujesz procedurę z [zasad projektu](../PROJECT_RULES.md) (część 6, „Poprawa podziału po Zadaniu 1”).

## Co oddajesz

Link do repozytorium i tag `task-1`. README zawiera uzupełnione sekcje „Problem i pytanie eksperymentalne”, „Dane i licencja” oraz „Protokół”. Repozytorium zawiera notebook albo skrypt audytu i pliki podziału.

## Jak oceniamy

* problem, pytanie i jednostka generalizacji: 20%;
* audyt danych, w tym liczba niezależnych jednostek: 25%;
* analiza wycieku danych i projekt podziału: 30%;
* metryka, seed, licencja i dokumentacja danych: 15%;
* czytelność repozytorium: 10%.

## Przed oddaniem sprawdź

1. Pliki z identyfikatorami train, validation i final test są w `splits/`.
2. W README jest tabela z liczbą przykładów i niezależnych jednostek w każdym zbiorze.
3. Commit ma tag `task-1` i tag jest wypchnięty na GitHub.
4. Żaden model nie był uruchamiany na final test.

[Pełne zasady projektu](../PROJECT_RULES.md)
