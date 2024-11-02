import streamlit as st
from models.model import Fruit
from streamlit_option_menu import option_menu
import requests
import time


#####################################################################################################################

shared_address = "http://localhost:8001/create_task"
master_url = "http://localhost:8000/send_command"

def create_task(fruits_list):
    response = requests.post(shared_address, json=fruits_list)
    return response
    

def receive_command():
    response = requests.get(master_url)
    return response



def MenuSalade():
    st.header("🍉 Choose Fruit For Your Salad")
    st.markdown("---")
    fruits_input = st.text_area("Enter your Order", key="fruits_input")

    # Convertir la chaine de caractère en liste
    fruits_list = [fruit.strip() for fruit in fruits_input.split(",") if fruit.strip()]
    # Convertir la liste en liste de dict
    fruits_list = [{"fruit": fruit_name} for fruit_name in fruits_list]
    
    col1, col2 = st.columns(2)
    command_btn = col1.button("Send Order")
    new_command_btn = col2.button("New Order")
    

    if command_btn:
        reponse = create_task(fruits_list)
        if reponse.status_code == 200:
            st.success("Your order has been processed. Please wait...")

        while True:
            time.sleep(4)
            reponse = receive_command()
            if reponse.status_code == 200:
                command = dict(reponse.json())
                st.success(f"{command.get('message')}\nPreparation time: {command.get('preparation_time')} secondes")
                break
            else:
                continue

    if new_command_btn:
        st.experimental_rerun()


        
        
        
    


def sidebBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Request a Salad"],
            icons=["house", "pencil"],
            menu_icon="cast",
            default_index=0
        )
    return selected

def main():
    st.set_page_config(page_title="Dashboard",page_icon="🍽",layout="wide")
    st.header("🍽 WELCOME TO OUR EXOTIC RESTAURANT")
    #st.markdown("#")

    with open("static/style/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.image("static/image/salade2.png", caption="Developed by MINN-GROUP", width=300)


    if "start_btn_clicked" not in st.session_state:
        # Initialiser la variable avec la valeur par défaut (False)
        st.session_state.start_btn_clicked = False

    # Vérifier si le bouton "Start" a été cliqué
    if not st.session_state.start_btn_clicked:
        start_btn = st.button("Start")
        if start_btn:
            # Une fois le bouton cliqué, on met à jour
            st.session_state.start_btn_clicked = True

    # Vérifier si le bouton "Start" a été cliqué avant d'afficher les autres parties de l'application
    if st.session_state.start_btn_clicked:
        selected = sidebBar()

        if selected == "Home":
            st.image("static/image/salade.png")
        
        elif selected == "Request a Salad":
            MenuSalade()

if __name__ == "__main__":
    main()