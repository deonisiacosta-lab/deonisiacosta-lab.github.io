import streamlit as st

st.title("✨ Supreza")

# Hatama naran
naran = st.text_input("Haruka Ita-nia Naran:", "Atou")

if naran.lower() == "atou":
    st.success("Parabéns Augusto Amaral! ! 🎉")
    
    # Hatama foto husi folder (porezemplu naran file mak "agus_foto.jpg")
    # Asegura katak file foto ne'e iha folder ne'ebé hanesan ho kódigu app.py
    st.image("Augusto Amaral.jpg", caption="Besik ona atu troka helem oan ne'e ho sapeu lulik😁😍")