import streamlit as st
import sqlite3

conn = sqlite3.connect('specimen_data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS specimen_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        microscope_size REAL NOT NULL,
        magnification REAL NOT NULL,
        real_life_size REAL NOT NULL
    )
''')
conn.commit()

st.title("🔬 Real-Life Specimen Size Calculator")

with st.form("specimen_form"):
    username = st.text_input("Your Name")
    microscope_size = st.number_input("Microscope Size (mm or µm)", format="%.4f")
    magnification = st.number_input("Magnification", min_value=0.01, format="%.2f")
    submitted = st.form_submit_button("Calculate and Save")

    if submitted:
        real_life_size = microscope_size / magnification
        cursor.execute('''
            INSERT INTO specimen_records (username, microscope_size, magnification, real_life_size)
            VALUES (?, ?, ?, ?)
        ''', (username, microscope_size, magnification, real_life_size))
        conn.commit()
        st.success(f"✅ Real-life size: {real_life_size:.4f} (Saved to DB)")

if st.checkbox("📁 Show Saved Records"):
    cursor.execute("SELECT username, microscope_size, magnification, real_life_size FROM specimen_records")
    rows = cursor.fetchall()
    st.dataframe(rows, use_container_width=True)
