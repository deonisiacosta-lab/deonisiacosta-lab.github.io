import streamlit as st

st.title("✨ Supreza")

# Hatama naran husi hasoru (user input)
naran = st.text_input("Haruka Ita-nia Naran:", "")

# Halo konversaun ba letre ki'ik hotu atu fasil to'o hikas iha match
naran_input = naran.strip().lower()

if naran_input == "atou" or naran_input == "augusto amaral":
    st.success("Parabéns Augusto Amaral! 🎉")
    st.image("Augusto Amaral.jpg", caption="Besik ona atu troka helem oan ne'e ho sapeu lulik😁😍")

elif naran_input == "deo":
    st.success("Parabéns Agus! 🌟")
    st.image("Kassa.jpg", caption="Tidak ada komentar") # Troka tuir naran foto ne'ebé iha Ita-nia folder

elif naran_input != "":
    st.warning("Deskulpa, naran ne'e la iha rejisitu ba foto espesiál.")
