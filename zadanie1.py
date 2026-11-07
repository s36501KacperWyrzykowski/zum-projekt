import os
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

print("--- SKRYPT ZADANIA 1 ---")

# 1. WCZYTANIE DANYCH
DATA_PATH = "male_players.csv"

if not os.path.exists(DATA_PATH):
  print(
      f"BŁĄD: Nie znaleziono pliku {DATA_PATH}"
  )
  exit()

print("Wczytywanie danych...")
df = pd.read_csv(DATA_PATH, low_memory=False)

# Filtrowanie wersji po FC 24
if "fifa_version" in df.columns:
  df = df[df["fifa_version"] == 24]

print(f"Liczba wierszy po wstępnym wczytaniu: {len(df)}")

# 2. AUDYT WSTĘPNY I STATYSTYKI TEKSTOWE
print("\n--- AUDYT WSTĘPNY DANYCH ---")
print(f"Liczba unikalnych zawodników (po ID): {df['player_id'].nunique()}")
duplicates = df.duplicated(subset=["player_id"]).sum()
print(f"Liczba zduplikowanych ID zawodników: {duplicates}")

# Usuwanie duplikatów po player_id
df = df.drop_duplicates(subset=["player_id"])

# Statystyki wejścia)
print("\n--- STATYSTYKI WEJŚCIA (TEKSTOWE) ---")
for col in ["player_traits", "player_positions"]:
  if col in df.columns:
    # Zamienianie na stringi (na wypadek braków) i liczenie długość znaków
    lengths = df[col].fillna("").astype(str).apply(len)
    print(
        f"Kolumna '{col}': średnia długość = {lengths.mean():.1f} znaków,"
        f" max = {lengths.max()} znaków"
    )

# Wyświetlenie kilku przykładowych zawodników z kluczowymi kolumnami
print("\n--- PRZYKŁADY ZAWODNIKÓW ---")
sample_cols = [
    "short_name",
    "overall",
    "wage_eur",
    "player_positions",
    "player_traits",
]
available_cols = [c for c in sample_cols if c in df.columns]
# Jeśli braki w kolumnach tekstowych, uzupełnianie pustym stringiem
df_display = df[available_cols].copy()
if "player_traits" in df_display.columns:
  df_display["player_traits"] = df_display["player_traits"].fillna("")
if "player_positions" in df_display.columns:
  df_display["player_positions"] = df_display["player_positions"].fillna("")

print(df_display.head(4).to_string(index=True))

# 3. CZYSZCZENIE BRAKÓW W KLUCZOWYCH KOLUMNACH (wolni agenci / brak zarobków)
group_col = "club_name"
if group_col in df.columns:
  df = df.dropna(subset=[group_col, "wage_eur"])
else:
  raise ValueError(f"Brak kolumny grupowej '{group_col}' w zbiorze danych!")

# 4. USUNIĘCIE WYCIEKÓW FINANSOWYCH
cols_to_drop = ["value_eur", "release_clause_eur"]
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

# 5. PODZIAŁ GRUPOWY (JEDNOSTKA GENERALIZACJI PO KLUBACH)
print("\nTworzenie podziału na Train, Validation i Final Test...")

gss_outer = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
train_val_idx, test_idx = next(
    gss_outer.split(df, groups=df[group_col])
)

df_train_val = df.iloc[train_val_idx].reset_index(drop=True)
df_test = df.iloc[test_idx].reset_index(drop=True)

gss_inner = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_idx, val_idx = next(
    gss_inner.split(df_train_val, groups=df_train_val[group_col])
)

df_train = df_train_val.iloc[train_idx].reset_index(drop=True)
df_val = df_train_val.iloc[val_idx].reset_index(drop=True)

# 6. WYZNACZENIE PROGÓW ZAROBKÓW WYŁĄCZNIE NA TRAIN
q25 = df_train["wage_eur"].quantile(0.25)
q75 = df_train["wage_eur"].quantile(0.75)

print(f"\nPróg 25% (Niski / Średni): {q25} EUR")
print(f"Próg 75% (Średni / Wysoki): {q75} EUR")


def assign_class(wage):
  if wage <= q25:
    return 0
  elif wage <= q75:
    return 1
  else:
    return 2


df_train["target_class"] = df_train["wage_eur"].apply(assign_class)
df_val["target_class"] = df_val["wage_eur"].apply(assign_class)
df_test["target_class"] = df_test["wage_eur"].apply(assign_class)

# 7. STATYSTYKI ZBIORÓW DLA PUNKTU 4
print("\n--- STATYSTYKI ZBIORÓW (PUNKT 4) ---")
for name, subset in [
    ("Train", df_train),
    ("Validation", df_val),
    ("Final Test", df_test),
]:
  n_samples = len(subset)
  n_clubs = subset["club_name"].nunique()
  print(f"Zbiór {name}:")
  print(f"  - Liczba przykładów (piłkarzy): {n_samples}")
  print(f"  - Liczba niezależnych jednostek (klubów): {n_clubs}")

# 8. ZAPIS PLIKÓW ID I PRÓBKI
os.makedirs("splits", exist_ok=True)
os.makedirs("data/sample", exist_ok=True)

df_train[["player_id"]].to_csv("splits/train_ids.csv", index=False)
df_val[["player_id"]].to_csv("splits/val_ids.csv", index=False)
df_test[["player_id"]].to_csv("splits/final_test_ids.csv", index=False)
df.head(100).to_csv("data/sample/sample_players.csv", index=False)

print("\nSukces! Pliki podziału zostały wygenerowane i zapisane w 'splits/'.")

# 9. WERYFIKACJA POPRAWNOŚCI PROTOKOŁU
print("\n--- URUCHAMIAM WERYFIKACJĘ PROTOKOŁU ---")
train_set = set(df_train["player_id"])
val_set = set(df_val["player_id"])
test_set = set(df_test["player_id"])

overlap_tv = train_set.intersection(val_set)
overlap_tt = train_set.intersection(test_set)
overlap_vt = val_set.intersection(test_set)

print(
    f"Wspólni zawodnicy Train <-> Val: {len(overlap_tv)} (Oczekiwano: 0)"
)
print(
    f"Wspólni zawodnicy Train <-> Test: {len(overlap_tt)} (Oczekiwano: 0)"
)
print(
    f"Wspólni zawodnicy Val <-> Test: {len(overlap_vt)} (Oczekiwano: 0)"
)

train_clubs = set(df_train["club_name"])
test_clubs = set(df_test["club_name"])
overlap_clubs = train_clubs.intersection(test_clubs)
print(
    f"Wspólne kluby Train <-> Final Test: {len(overlap_clubs)} (Oczekiwano: 0)"
)

print(
    "\nWeryfikacja zakończona! Pliki są gotowe."
)
