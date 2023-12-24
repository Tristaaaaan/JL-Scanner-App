import requests
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import RoundedRectangle, Color
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.popup import Popup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading
import telebot
import time

# Replace with your Telegram Bot API token
TELEGRAM_API_TOKEN = '6677396383:AAFGIQb6l0Ec6Z0Vg3ymEdNKrlMCopxgYVo'

# Set up Google Sheets API
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Define the credentials directly as Python dictionaries
credentials_dict = {
   "type": "service_account",
   "project_id": "cektoko",
   "private_key_id": "132cfa13b885a7b6826ce67b656cea30947f76b9",
   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwuXFWB8w9bAGs\ns4VnFteQ6cuAgvMhafSGCPgk7el2VrrPVPx1rzpcJujUXk4Q8bXrQaSMCRyP22Ai\n6Xay1hjmId2bSBYEDfleCiRi9jpQU3bnDfccn9hKMrY4+uhEiCv+dkuzZ6eP6FTT\nJBQ7UFvYpd+wqoAV7SvwinEIv0g+2h4ijylyXRyv3izWbUfUa8tAbtWAKQNSTk0H\n0GTHrVB24iXEsTcxqk398qEaYN4j5wkvpKI8BGsBoorhNZcol/7rG2M1Ih/HDcdY\naloMKUSRoExcBIIugPFqXy44A0cADFgkWtRaodvP+uoQNEYxj/IhvWMWWxtDjsKu\nkNHtwrndAgMBAAECggEAD5RRjv2B/loyrZhn5sYnO9G4jHw+1c/C7DwHMC4/Gh0c\nO+HonbFUakJN3UbxB+JfIL25NVUqTO5Qg9NkEPD54fPTVvicZEAdHzKysXy2eFVb\nUpQzGDVpOmVNFincZwpAIp8oHklBhti6/aAdHnt/lVJOLYNiZkxxxrNVsqk2Q8AO\nDXzPR5Is9ORQOUMYj232R9IVBQSYZltD8bx0fwTuUAtk2LfJTmibIAQfD3efmU6U\ncNN6a0Op4Lsd8lVqlmVOzJdt1WUNvjGot/djyC5WLYdSrqOtS5XV6QKAbPvzFQG4\nSsUpHs4+HL/2dcM94H+40Ezr+Q9JMMOFEBS5CYyeOwKBgQDu7KL2TlDAgtIG5OEy\nA2+vRCa1GuoAupl3WnhJn/RxcVDwWunBuQoXQz++to7lBndh/ZE274tSmunVndGF\nUzTZQhgBq4OHKmACn2C5rVczfLv5roOb31kxHrt+bXLvEVs1Fqay3+mDvSNhMx5o\nV1YUzBno6N4u+ky6vdk6FZHh7wKBgQC9WstmDt7Dl5QV7BU7Y9OZ0Ba6aXj+QJus\n7yYR6u6rtkms3hYm7GOeXVO5wP7g0Grx/qhsFebd2bpW87SsN6B2mLgfxHfL+nFV\nbuFcJvwlKPEp2RD51pUbpaL1W7p1AGcJpGzzr8mEifGDVkk3K55pcPH1wjPSppZW\nkElM/j788wKBgG0DDz+ub+3GQqnemFlHdBfV0otjYk0+1nK8lpGRJ+jyuOlRscIv\n+Uiv6E/N39jjYGkXVsBn/3uLLxHGViis1Doki+uHJBXx4aiQq4NMcbMOQH4lf+sI\ntxtQWF/Q9FXb52+LjDelLlhrXc8lkcQtxRrsHQ5F4coxbfzuTkTQPqWFAoGAdyyQ\nvT/4pgNdeVqnlkRi5fiYhWRieSryj6nIPRiudDX7MqhoKsE2hXJZgpxcDeQ+muXa\n3IQAVHp3E8i4Wnd8L4g4wg2mFCQgdlOd1KDYqw6UkfEDBSsvl0HtSR0dQgwpzWDG\nDa0CWL902GNTGz0Bq30hW7qJYTflgL+40pNl008CgYEAlPI/qCyG8UzxXF7yCPU9\nqdJ9E/mr6EJJXplhgueawpNf/wiCFqu3DfTwtt54jeobjCSKouR7mvYclYrwNfER\nLzy6teNcQpxzjcNJoEVpUubRqwV3PzKUw3TXcvznQp58FimBtIlYOtUKh1NLoYYp\nzNlkDjBpbXH+J43CKoBtuAI=\n-----END PRIVATE KEY-----\n",
   "client_email": "cektoko@cektoko.iam.gserviceaccount.com",
   "client_id": "111330192017501329790",
   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
   "token_uri": "https://oauth2.googleapis.com/token",
   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cektoko%40cektoko.iam.gserviceaccount.com",
   "universe_domain": "googleapis.com"
}

other_credentials_dict = {
   "type": "service_account",
   "project_id": "cektoko",
   "private_key_id": "132cfa13b885a7b6826ce67b656cea30947f76b9",
   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwuXFWB8w9bAGs\ns4VnFteQ6cuAgvMhafSGCPgk7el2VrrPVPx1rzpcJujUXk4Q8bXrQaSMCRyP22Ai\n6Xay1hjmId2bSBYEDfleCiRi9jpQU3bnDfccn9hKMrY4+uhEiCv+dkuzZ6eP6FTT\nJBQ7UFvYpd+wqoAV7SvwinEIv0g+2h4ijylyXRyv3izWbUfUa8tAbtWAKQNSTk0H\n0GTHrVB24iXEsTcxqk398qEaYN4j5wkvpKI8BGsBoorhNZcol/7rG2M1Ih/HDcdY\naloMKUSRoExcBIIugPFqXy44A0cADFgkWtRaodvP+uoQNEYxj/IhvWMWWxtDjsKu\nkNHtwrndAgMBAAECggEAD5RRjv2B/loyrZhn5sYnO9G4jHw+1c/C7DwHMC4/Gh0c\nO+HonbFUakJN3UbxB+JfIL25NVUqTO5Qg9NkEPD54fPTVvicZEAdHzKysXy2eFVb\nUpQzGDVpOmVNFincZwpAIp8oHklBhti6/aAdHnt/lVJOLYNiZkxxxrNVsqk2Q8AO\nDXzPR5Is9ORQOUMYj232R9IVBQSYZltD8bx0fwTuUAtk2LfJTmibIAQfD3efmU6U\ncNN6a0Op4Lsd8lVqlmVOzJdt1WUNvjGot/djyC5WLYdSrqOtS5XV6QKAbPvzFQG4\nSsUpHs4+HL/2dcM94H+40Ezr+Q9JMMOFEBS5CYyeOwKBgQDu7KL2TlDAgtIG5OEy\nA2+vRCa1GuoAupl3WnhJn/RxcVDwWunBuQoXQz++to7lBndh/ZE274tSmunVndGF\nUzTZQhgBq4OHKmACn2C5rVczfLv5roOb31kxHrt+bXLvEVs1Fqay3+mDvSNhMx5o\nV1YUzBno6N4u+ky6vdk6FZHh7wKBgQC9WstmDt7Dl5QV7BU7Y9OZ0Ba6aXj+QJus\n7yYR6u6rtkms3hYm7GOeXVO5wP7g0Grx/qhsFebd2bpW87SsN6B2mLgfxHfL+nFV\nbuFcJvwlKPEp2RD51pUbpaL1W7p1AGcJpGzzr8mEifGDVkk3K55pcPH1wjPSppZW\nkElM/j788wKBgG0DDz+ub+3GQqnemFlHdBfV0otjYk0+1nK8lpGRJ+jyuOlRscIv\n+Uiv6E/N39jjYGkXVsBn/3uLLxHGViis1Doki+uHJBXx4aiQq4NMcbMOQH4lf+sI\ntxtQWF/Q9FXb52+LjDelLlhrXc8lkcQtxRrsHQ5F4coxbfzuTkTQPqWFAoGAdyyQ\nvT/4pgNdeVqnlkRi5fiYhWRieSryj6nIPRiudDX7MqhoKsE2hXJZgpxcDeQ+muXa\n3IQAVHp3E8i4Wnd8L4g4wg2mFCQgdlOd1KDYqw6UkfEDBSsvl0HtSR0dQgwpzWDG\nDa0CWL902GNTGz0Bq30hW7qJYTflgL+40pNl008CgYEAlPI/qCyG8UzxXF7yCPU9\nqdJ9E/mr6EJJXplhgueawpNf/wiCFqu3DfTwtt54jeobjCSKouR7mvYclYrwNfER\nLzy6teNcQpxzjcNJoEVpUubRqwV3PzKUw3TXcvznQp58FimBtIlYOtUKh1NLoYYp\nzNlkDjBpbXH+J43CKoBtuAI=\n-----END PRIVATE KEY-----\n",
   "client_email": "cektoko@cektoko.iam.gserviceaccount.com",
   "client_id": "111330192017501329790",
   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
   "token_uri": "https://oauth2.googleapis.com/token",
   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cektoko%40cektoko.iam.gserviceaccount.com",
   "universe_domain": "googleapis.com"
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)
client = gspread.authorize(credentials)
# Authenticate using the other credentials file
other_credentials = ServiceAccountCredentials.from_json_keyfile_dict(other_credentials_dict, SCOPE)
other_client = gspread.authorize(other_credentials)


OTHER_SPREADSHEET_ID = '16LSKlSs2aSfq_5dIE7pezO0cy5T40mvQOiaqGFh_eSQ'


# Open the other Google Spreadsheet by ID
other_spreadsheet = other_client.open_by_key(OTHER_SPREADSHEET_ID)

# Fetch chat IDs from a specific sheet in the other spreadsheet
other_sheet_name = 'CHAT_ID'  # Change this to the name of the sheet in the other spreadsheet
other_chat_ids = [chat_id[0] for chat_id in other_spreadsheet.worksheet(other_sheet_name).get_all_values()]

# Use the other_chat_ids in your code
CHAT_IDS = other_chat_ids


# Open the Google Spreadsheet by ID
SPREADSHEET_ID = '1XLJUkSN41ziKdpZIhGDd98DScIDVkcbkKTD6OykgU_Q'
spreadsheet = client.open_by_key(SPREADSHEET_ID)

# Telkomsel user agent
telkomsel_user_agent = "Mozilla/5.0 (Linux; Android 11; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36"

# Initialize Telebot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# Function to check SSL validity
def check_ssl_validity(domain):
    try:
        response = requests.get("https://{}".format(domain), headers={"User-Agent": telkomsel_user_agent})
        response.raise_for_status()
        return True
    except requests.exceptions.SSLError:
        return False
    except requests.exceptions.RequestException:
        return None

class SSLCheckerApp(App):
    def build(self):
        # Main layout (RelativeLayout for centering)
        main_layout = RelativeLayout()

        # Centered BoxLayout
        center_layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(None, None),
            pos_hint={'center_x': 0.4, 'center_y': 0.5},  # Center the layout both horizontally and vertically
        )

        # Logo image (larger size)
        logo_url = 'https://i.ibb.co/cCBQ1qx/logo.png'  # Replace with your logo URL
        logo = AsyncImage(source=logo_url, size_hint=(None, None), size=(300, 300))

        # Start button
        self.start_button = Button(
            text='Start Proses',
            size_hint=(None, None),  # Ensure button size isn't affected by text
            size=(300, 150),
            background_color=(0.2, 0.8, 0.2, 1)  # Set the background color to green
        )
        self.start_button.bind(on_press=self.start_checking)

        # Stop button
        self.stop_button = Button(
            text='Stop Proses',
            size_hint=(None, None),  # Ensure button size isn't affected by text
            size=(300, 150),
            background_color=(0.8, 0.2, 0.2, 1)  # Set the background color to red
        )
        self.stop_button.bind(on_press=self.stop_checking)
        self.stop_button.disabled = True

        # Scanning label
        self.scanning_label = Label(
            text='Scanning...',
            opacity=0,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'y': 0}  # Centered at the bottom
        )

        # Add widgets to the centered layout
        center_layout.add_widget(logo)
        center_layout.add_widget(self.start_button)
        center_layout.add_widget(self.stop_button)
        center_layout.add_widget(self.scanning_label)

        # Add the centered layout to the main layout
        main_layout.add_widget(center_layout)

        return main_layout


    def round_button(self, button):
        radius = [10, 10, 10, 10]  # Adjust the values for the desired roundness
        with button.canvas.before:
            Color(1, 1, 1)  # Set the color of the button background
            RoundedRectangle(pos=button.pos, size=button.size, radius=radius)


    def start_checking(self, instance):
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.scanning_label.opacity = 1
        self.check_ssl_thread = threading.Thread(target=self.check_ssl_loop)
        self.check_ssl_thread.daemon = True
        self.check_ssl_thread.start()

    def stop_checking(self, instance):
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.scanning_label.opacity = 0

    def check_ssl_loop(self):
        while self.stop_button.disabled is False:
            try:
                for tab_name in sheet_tabs:
                    sheet = spreadsheet.worksheet(tab_name)
                    domains_to_check = [domain[0] for domain in sheet.get_all_values()]
                    for domain in domains_to_check:
                        if not check_ssl_validity(domain):
                            self.push_notification(tab_name, domain)
                time.sleep(120)
            except Exception as e:
                print(f"An error occurred: {e}")

    def push_notification(self, category, domain):
        message = f"URGENT COI:\n({category}) - {domain}  \nSTATUS : 🔴NAWALA !"

        # Send Telegram notifications
        telegram_message = f"URGENT COI:\n({category}) - {domain}  \nSTATUS : 🔴NAWALA !"
        for chat_id in CHAT_IDS:
            bot.send_message(chat_id, telegram_message)
            print(f"Telegram notification sent for {domain} in {category} to {chat_id}")


if __name__ == '__main__':
    sheet_tabs = [sheet.title for sheet in spreadsheet.worksheets()]
    SSLCheckerApp().run()
