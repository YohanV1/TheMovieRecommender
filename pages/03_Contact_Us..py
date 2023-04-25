import streamlit as st
from send_email import send_email

st.title("Contact Us")
st.write("If you would like to contribute to the content of the app, "
         "such as submitting reviews, "
         "suggesting new movies to be added to the "
         "database, or adding information about lesser-known movies, "
         "please feel free to get in touch!")

with st.form(key="email_form", clear_on_submit=True):
    user_email = st.text_input("Your email address")
    message = st.text_area("Your message")
    subject = f"New email from {user_email}"
    button = st.form_submit_button("Submit")
    if button:
        send_email(message, subject)
        st.info("Your message was sent successfully.")
