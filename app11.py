import streamlit as st
import subprocess
from PIL import Image
import os
import pyrebase
import requests
import json
import speech_recognition as sr
import base64

# Set page configuration
st.set_page_config(
    page_title="HomeMapper",
    page_icon=":cyclone:",
    layout="wide"
)

# Firebase configuration (your existing Firebase config)
firebaseConfig = {
    'apiKey': "AIzaSyB_7P-uGwj-veIRQ6r0pmvYt3icC4g5zrU",
    'authDomain': "homemapper-f7f6f.firebaseapp.com",
    'projectId': "homemapper-f7f6f",
    'databaseURL': "https://homemapper-f7f6f-default-rtdb.europe-west1.firebasedatabase.app",
    'storageBucket': "homemapper-f7f6f.appspot.com",
    'messagingSenderId': "1066817282093",
    'appId': "1:1066817282093:web:077ea42f354a7b073558a4",
    'measurementId': "G-SVZPN84TEH"
}

# Firebase authentication initialization
import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def sidebar_bg(side_bg):
    side_bg_ext = 'gif'
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def run_blender_script(description, output_image_path):
    script_path = "render.py"  # Ensure this is the correct path to your render.py
    create_output_dir(os.path.dirname(output_image_path))  # Create output directory if not exists
    subprocess.run(["blender", "--background", "--python", script_path, "--", description, output_image_path])

def speak():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please Speak..")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            st.write("Sorry, could not recognize your speech.")

def main():
    st.sidebar.title("HomeMapper")
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up'])
    email = st.sidebar.text_input("User Email")
    password = st.sidebar.text_input('Password', type='password')

    if choice == 'Sign up':
        handle = st.sidebar.text_input('User name', value='Default')
        submit = st.sidebar.button('Create Account')

        if submit:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success('Account Successfully Created!')
                st.balloons()
                user = auth.sign_in_with_email_and_password(email, password)
                db = firebase.database()
                db.child(user['localId']).child("Handle").set(handle)
                db.child(user['localId']).child("ID").set(user['localId'])
                st.title('Hello ' + handle)
            except requests.exceptions.HTTPError as e:
                error_message = e.args[0]
                error_json = json.loads(error_message.response.text)
                st.error(f"Error: {error_json['error']['message']}")

    if choice == "Login":
        login = st.sidebar.checkbox('Login')
        if login:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success(' Welcome')
            st.balloons()

            # Set background and sidebar
            st.markdown(
                """
                <style>
                .stApp {{
                    background: url("./g2.gif");
                    background-size: cover
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            sidebar_bg('./ga.jpg')
            st.write('---')

            # Left and Right columns
            col_left, col_right = st.columns([5, 4])

            with col_left:
                if "speech_txt" not in st.session_state:
                    st.session_state['speech_txt'] = "Please enter text"

                if st.button('Speak'):
                    text = speak()
                    st.session_state['speech_txt'] = text

                # Floor Plan Description
                user_input = st.text_area("Floor Plan Description", st.session_state['speech_txt'])

                output_image_path = 'C:/Users/Raheem/Downloads/ADditonal/Test/HomeMapper_F/floor_plan.png'

                if st.button("Generate 3D Model"):
                    run_blender_script(user_input, output_image_path)
                    if os.path.exists(output_image_path):
                        st.image(Image.open(output_image_path), width=550)
                    else:
                        st.error("Failed to generate the 3D model. Please check the Blender script.")
            with col_right:
                # Additional content on the right column
                st.write("Additional content on the right column goes here.")

if __name__ == "__main__":
    main()
