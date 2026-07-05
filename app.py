import streamlit as st
import pandas as pd
import joblib

# 1. Wczytanie naszego zapisanego modelu
model = joblib.load('model_churn_rf.pkl')

# 2. Ustawienia wyglądu strony
st.set_page_config(page_title="Asystent Retencji", page_icon="📉")
st.title("📉 Kalkulator Ryzyka Odejścia Klienta")
st.write("Wprowadź dane z profilu klienta, aby oszacować ryzyko jego rezygnacji z usług.")

# 3. Interfejs użytkownika (suwaki i pola wyboru)
st.sidebar.header("Dane Klienta")

# Skupiamy się na 3 najważniejszych zmiennych, które wykrył nasz model
tenure = st.sidebar.slider("Staż klienta (miesiące)", min_value=0, max_value=72, value=12)
monthly_charges = st.sidebar.slider("Miesięczny rachunek (PLN)", min_value=15.0, max_value=120.0, value=50.0)
total_charges = st.sidebar.number_input("Całkowite dotychczasowe opłaty (PLN)", min_value=0.0, value=600.0)

# Dodatkowe pola, żeby model miał komplet danych (uproszczenie)
contract_type = st.sidebar.selectbox("Typ umowy", ["Month-to-month", "One year", "Two year"])

# 4. Przycisk wyzwalający obliczenia
if st.button("Analizuj Ryzyko"):

    # --- ZAPLECZE INŻYNIERSKIE ---
    # Model oczekuje dokładnie 30 kolumn (takich jak w X_train po get_dummies).
    # Tworzymy "pustą" tabelę wypełnioną zerami, która ma taki sam układ jak dane treningowe.
    # W prawdziwym wdrożeniu wszystkie te pola byłyby pobierane z bazy danych.

    cechy_modelu = model.feature_names_in_
    dane_wejsciowe = pd.DataFrame(0, index=[0], columns=cechy_modelu)

    # Podmieniamy zera na to, co doradca wpisał w aplikacji
    dane_wejsciowe['tenure'] = tenure
    dane_wejsciowe['MonthlyCharges'] = monthly_charges
    dane_wejsciowe['TotalCharges'] = total_charges

    # Obsługa One-Hot Encoding dla typu umowy
    if contract_type == "One year" and 'Contract_One year' in dane_wejsciowe.columns:
        dane_wejsciowe['Contract_One year'] = 1
    elif contract_type == "Two year" and 'Contract_Two year' in dane_wejsciowe.columns:
        dane_wejsciowe['Contract_Two year'] = 1

    # 5. Odpytanie modelu (nasz Próg 30%)
    ryzyko = model.predict_proba(dane_wejsciowe)[0][1]  # Pobieramy procent dla klasy '1'

    # 6. Wyświetlenie pięknego wyniku na stronie
    st.subheader("Wynik Analizy:")

    if ryzyko >= 0.30:
        st.error(f"⚠️ ALARM! Ryzyko odejścia wynosi {ryzyko * 100:.1f}%.")
        st.write(
            "**Rekomendacja dla doradcy:** Ryzyko przekracza próg 30%. Natychmiast zaoferuj klientowi zniżkę lojalnościową lub dodatkowy pakiet usług.")
    else:
        st.success(f"✅ Klient jest stabilny. Ryzyko odejścia to tylko {ryzyko * 100:.1f}%.")
        st.write("**Rekomendacja dla doradcy:** Brak wskazań do interwencji rabatowej.")

    #do ponownego otwarcia w terminalu wpisz .venv\Scripts\activate zeby wczytac potrzebne biblioteki, natomiast zeby odpalic to streamlit run app.py
    #G sugeruje nagrannie gifa przy wstawianiu na githuba z uzcyiem nagrania program o nazwie ScreenToGif