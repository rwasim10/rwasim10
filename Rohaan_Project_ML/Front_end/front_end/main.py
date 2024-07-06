import streamlit as st
import requests
import os

def main():
    st.markdown("""
    <div style="text-align: center;">
    <h1>Your Weight & You</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center;">
    Understanding your weight, empowering your wellness
    </div>
    """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'token' not in st.session_state:
        st.session_state['token'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    base_url = os.getenv('API_URL', 'http://127.0.0.1:8000')

    if not st.session_state['logged_in']:
        login_or_register(base_url)
    else:
        st.sidebar.write(f"Logged in as {st.session_state['username']}")
        bmi = show_bmi_calculator(base_url)
        if bmi:
            show_bmi_suggestions(base_url, bmi)
        logout_button()

def login_or_register(base_url):
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login_page(base_url)
    elif choice == "Register":
        register_page(base_url)

#response = requests.post(f"{base_url}/login/?username={username}&password={password}")
def login_page(base_url):
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if not username or not password:
            st.error("Username and password are required.")
            return
        try:
            response = requests.post(f"{base_url}/login/?username={username}&password={password}")
            response.raise_for_status()
            
            st.session_state['logged_in'] = True
            st.session_state['token'] = response.json()['token']
            st.session_state['username'] = username
            st.success("Login successful!")
            st.experimental_rerun()
        except requests.exceptions.HTTPError as err:
            st.error(f"Login Failed: {err.response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as err:
            st.error(f"An error occurred: {err}")

#response = requests.post(f"{base_url}/register/?username={new_username}&password={new_password}&password_confirm={confirm_password}&email={email}")
def register_page(base_url):
    st.subheader("Create Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    email = st.text_input("Email Address")
    
    if st.button("Register"):
        if not new_username or not new_password or not confirm_password or not email:
            st.error("All fields are required.")
            return
        if new_password != confirm_password:
            st.error("Password confirmation doesn't match password.")
            return
        try:
            response = requests.post(f"{base_url}/register/?username={new_username}&password={new_password}&password_confirm={confirm_password}&email={email}")
            response.raise_for_status()
            st.success("Registration Successful!")
            st.write("You can now login with your new account.")
            st.info("A confirmation email has been sent to your email address.")
        except requests.exceptions.HTTPError as err:
            st.error(f"Registration Failed: {err.response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as err:
            st.error(f"An error occurred: {err}")

#response = requests.post(f"{base_url}/bmi/?weight={weight}&height_ft={height_ft}&height_in={height_in}", headers=headers)
def show_bmi_calculator(base_url):
    st.markdown("""
    <div style="text-align: center;">
    Health Check: Assess weight quickly for health risks
    Risk Indicator: Flags underweight, overweight, or obesity
    Tracking Tool: Monitors weight status for health management
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Calculate Your BMI")
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    height_ft = st.number_input("Height (ft)", min_value=0, step=1)
    height_in = st.number_input("Height (in)", min_value=0, step=1)

    if st.button("Calculate BMI"):
        if weight <= 0 or height_ft <= 0:
            st.error("Weight and height must be greater than zero.")
            return
        try:
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            response = requests.post(f"{base_url}/bmi/?weight={weight}&height_ft={height_ft}&height_in={height_in}", headers=headers)
            response.raise_for_status()
            bmi = response.json()['bmi']
            st.success(f"Your BMI is {bmi:.2f}")
            return bmi
        except requests.exceptions.HTTPError as err:
            st.error(f"Calculation Failed: {err.response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as err:
            st.error(f"An error occurred: {err}")

#response = requests.post(f"{base_url}/bmi_result_suggestions/?topic_input={topic_input}")
def show_bmi_suggestions(base_url, bmi):
    st.subheader("Get BMI Result Suggestions")
    topic_input = bmi
    if not topic_input:
        st.error("BMI result is required.")
        return
    try:
        token = st.session_state.get('token')
        if not token:
            st.error("Authentication token not found.")
            return
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        with st.spinner('Generating Result....'):
            response = requests.post(f"{base_url}/bmi_result_suggestions/?topic_input={topic_input}")
            response.raise_for_status()
            suggestions = response.json().get('bmi')
            st.session_state.bmi = suggestions
            st.success("Suggestions generated successfully!")
            st.write(f"BMI Value: {topic_input}")
            st.write("Suggestions:")
            st.write(suggestions)
    except requests.exceptions.HTTPError as err:
        st.error(f"Suggestion Generation Failed: {err.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def logout_button():
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('token', None)
        st.session_state.pop('username', None)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
