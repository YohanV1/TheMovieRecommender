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

st.sidebar.title("The Movie Recommender.")
with st.sidebar.expander("About"):
    st.write(f"The Movie Recommender uses cosine similarity to suggest "
                 f"movies based on user input. The system "
                 f"is built using TMDB's 5000 movie dataset. Additional information is "
                 f"retrieved from TMDB's API."
                 f" This project was initiated for a course at my university"
                 f" and is still a work in progress. If you would like to give"
                 f" feedback or contribute, the source code and documentation "
                 f"for the project can be found "
                 f"[here](https://github.com/YohanV1/TheMovieRecommender)."
                 f" If you have any suggestions or questions, "
                 f"please don't hesitate to reach out.")