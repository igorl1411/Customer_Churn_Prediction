#  Customer Churn Prediction: Random Forest & Threshold Tuning

## O projekcie
Projekt analityczny mający na celu przewidywanie odejść klientów (Customer Churn) w sektorze telekomunikacyjnym. Głównym założeniem było zbudowanie modelu uczenia maszynowego, który odchodzi od optymalizacji czystej dokładności (Accuracy) na rzecz optymalizacji **Czułości (Recall)**, minimalizując tym samym straty biznesowe wynikające z tzw. False Negatives (przegapionych uciekinierów).

## Technologie i Narzędzia
* **Język:** Python 3
* **Środowisko:** Jupyter Notebook
* **Biblioteki:** `pandas`, `matplotlib`, `seaborn`, `scikit-learn`
* **Algorytm główny:** Random Forest Classifier (Las Losowy)

## Dane i Preprocessing
Wykorzystano ustandaryzowany zbiór danych *Telco Customer Churn* (>7000 rekordów). 
* **Data Cleaning:** Naprawa błędnych typów tekstowych na numeryczne (`TotalCharges`), usunięcie szumu informacyjnego (`customerID`).
* **Encoding:** Konwersja zmiennych kategorycznych za pomocą techniki One-Hot Encoding (`drop_first=True` w celu uniknięcia pułapki idealnej współliniowości).

## Metodologia i Wyniki Modelowania

### 1. Model Bazowy
Wytrenowano standardowy model Lasu Losowego ze 100 estymatorami. 
* **Accuracy:** ~79.3%
* **Wniosek:** Ze względu na niezbalansowanie klas (znaczna przewaga klientów pozostających), model faworyzował klasę większościową. Czułość (Recall) dla odchodzących klientów wyniosła zaledwie **47.8%**. Model wyłapał mniej niż połowę faktycznych rezygnacji.

### 2. Próba naprawy: Class Weights
Wdrożono parametr `class_weight='balanced'`, aby wymusić na algorytmie większą uwagę na klasę mniejszościową.
* **Wynik:** Brak poprawy. Recall spadł do **~45%**. Algorytm Random Forest okazał się wysoce odporny na matematyczne wagi przy tej strukturze danych. Wymagało to przejścia na poziom optymalizacji logiki decyzyjnej.

### 3. Optymalizacja Biznesowa (Threshold Tuning)
W branży telekomunikacyjnej asymetria kosztów jest wyraźna: koszt zaoferowania niepotrzebnego rabatu (False Positive) jest niższy niż utrata klienta (False Negative). Zastosowano manualne przesunięcie progu odcięcia (Decision Threshold).
* **Akcja:** Zamiast domyślnego progu 50%, nakazano algorytmowi flagować klientów jako odchodzących już przy **30% przewidywanego ryzyka**.
* **Nowe Wyniki:** Czułość (Recall) drastycznie wzrosła z 48% do **74%**. Zwiększono liczbę wyłapanych rezygnacji z 219 do 337 (na zbiorze testowym), dostarczając zespołowi utrzymania (Retention Team) znacznie szerszą bazę do ratowania budżetu.

## Kluczowe czynniki rezygnacji (Feature Importance)
Model zidentyfikował trzy główne zmienne napędzające ucieczkę klientów:
1. `TotalCharges` (Całkowite opłaty)
2. `MonthlyCharges` (Miesięczny rachunek)
3. `Tenure` (Staż klienta)

##  Podsumowanie
Projekt demonstruje pełen cykl życia modelu: od czyszczenia danych, poprzez ewaluację problemu niezbalansowanych klas (Class Imbalance) i weryfikację wag, aż po optymalizację decyzji opartą na realiach i kosztach biznesowych.
