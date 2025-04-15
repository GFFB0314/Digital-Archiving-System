import sqlite3
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
import sys
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.textinput import TextInput
from kivymd.uix.gridlayout import GridLayout, MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
import os
from kivymd.uix.divider import MDDivider
from kivy.clock import Clock
from kivymd.uix.widget import Widget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import (
    MDTextFieldMaxLengthText,
    MDTextFieldTrailingIcon,
    MDTextFieldLeadingIcon,
    MDTextFieldHelperText,
    MDTextFieldHintText,
    MDTextField,
)
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from fpdf import FPDF

# from fpdf.enums import XPos, YPos
import subprocess  # Import the subprocess module


class WelcomeScreen(Screen):
    pass


class edit_form_filling_no_leasing(Screen):
    pass


class edit_form_filling_leasing(Screen):
    pass


class LoginScreen(Screen):
    pass


class SearchScreen(Screen):
    pass


class SearchScreen2(Screen):
    pass


class form_filling_yes_leasing(Screen):
    pass


class About_Us(Screen):
    pass


class form_filling_no_leasing(Screen):
    pass


class MenuScreen(Screen):
    pass


class MenuScreen2(Screen):
    pass


class ViewRecordScreen(Screen):
    pass


class MenuScreen3(Screen):
    pass


# Window.fullscreen = True


# Decorator giving app exiting information
def infos(func):
    def wrapper(self, *args, **kwargs):
        print("About to leave the App")
        func(
            self, *args, **kwargs
        )  # Call the original method with self and any other args/kwargs
        print("Left the App!")

    return wrapper


# Class to create a PDF FILE
class CustomPDF(FPDF):
    def header(self):
        # Get the absolute path of the image file
        image_path = os.path.join(os.path.dirname(__file__), "Image", "smart.jpg")

        # Set up the title and logo for the header
        image_x_coordinate = self.w - 50  # Calculating the X coordinate of the image

        self.image(image_path, image_x_coordinate, 2, 40)  # x, y coordinate and width

        self.set_font("Times", "BU", 17)  # font, style, size
        # self.set_draw_color(15, 20, 25)
        # self.set_text_color(250, 50, 50)

        title = "TECHNICAL INTERVENTION SHEET"
        title_w = self.get_string_width(title) + 5
        # self.set_x()
        # self.set_y(25)

        self.cell(title_w, 10, title, border=1, align="C", fill=0)
        self.ln(27)

    def table_vertical(self, data: list):
        # Set up the vertical table structure for each form entry
        self.set_font("Helvetica", "", 12)
        header_background_color = (200, 150, 150)
        # self.ln(10) # Changed
        for row in data:
            for header, value in row.items():
                self.set_fill_color(*header_background_color)
                self.set_text_color(5, 4, 4)
                self.cell(40, 10, header, border=1, align="C", fill=True, ln=0)
                self.cell(0, 10, str(value), border=1, align="C", ln=1)
            self.ln(5)

    def footer(self):
        # Set up the footer with the page number
        self.set_y(-15)
        self.set_font("Times", "BI", 10)
        self.cell(0, 10, f"{self.page_no()} / {{nb}}", align="C")


ROOT_FOLDER = r"C:\Archive"  # Where all files and folders are going to be saved
OBJECTS = (
    "INSTALLATION",
    "DESINSTALLATION",
    "REINSTALLATION",
    "MAINTENANCE",
    "CALIBRATION",
)
MAINTENANCE_OPTIONS = (
    "SIM_CHANGE",
    "CAST_CHANGE",
    "RAS",
    "ANTENNA_CHANGE",
    "BADGE_CHANGE",
    "DRIVE_CHANGE",
    "RELAY_CHANGE",
    "VEH_NOT_RECEI",
    "REBOOTING",
    "CORRECTED INSTAL",
    "GSM DEFAULT",
)


class MyApp(MDApp):

    def init_database(self):
        # Determine the correct base path for the database
        if getattr(sys, "frozen", False):
            # Running as EXE - use the executable's directory
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as script - use the script's directory
            base_path = os.path.dirname(__file__)

        # Create a dedicated 'data' subdirectory if it doesn't exist
        data_dir = os.path.join(base_path, "data")
        os.makedirs(data_dir, exist_ok=True)

        # Database path in the persistent data directory
        self.db_path = os.path.join(data_dir, "archive.db")

        # Connect to the database (creates if doesn't exist)
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Create tables if they don't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS archives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_type TEXT NOT NULL,
                client_name TEXT NOT NULL,
                locataire TEXT,
                immat TEXT,
                last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version INTEGER DEFAULT 1,
                object TEXT,
                cast_type TEXT,
                serial_number TEXT,
                doi TEXT,
                imei TEXT,
                device_id TEXT,
                vehicle_type TEXT,
                chassis TEXT,
                iccid TEXT,
                technician_name TEXT,
                maintenance_opt TEXT,
                pdf_data BLOB NOT NULL
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'editor', 'viewer')),
                last_login TIMESTAMP
            )
        """
        )

        # Insert default root user if not exists
        cursor.execute(
            """
            INSERT OR IGNORE INTO users (user_name, password, role) 
            VALUES (?, ?, ?)
        """,
            ("root", "root", "admin"),
        )

        self.conn.commit()
        print(f"Database initialized at: {self.db_path}")

    def build(self) -> ScreenManager:
        self.icon = os.path.join(os.path.dirname(__file__), "Image", "xSAVECir.jpg")
        self.title = "xSAVE"
        self.init_database()
        self.theme_cls.primary_palette = "Thistle"  # Olive is also very appealing
        self.theme_cls.accent_palette = "Purple"
        # self.theme_cls.theme_style = "Dark"
        # Initialize ScreenManager with NoTransition
        self.sm = ScreenManager(transition=NoTransition())

        # Load the KV file here, after the MDApp has been initialized
        Builder.load_file("main.kv")

        self.screen_history: list = (
            []
        )  # Initialize the navigation stack to keep track of the visited screens

        # Add the screens to the ScreenManager
        screens = [
            WelcomeScreen(name="welcome"),
            LoginScreen(name="login"),
            MenuScreen(name="menu"),
            MenuScreen2(name="menu2"),
            MenuScreen3(name="menu3"),
            SearchScreen(name="search"),
            SearchScreen2(name="search2"),
            ViewRecordScreen(name="view_record_screen"),
            form_filling_yes_leasing(name="leasing"),
            edit_form_filling_no_leasing(name="edit_no_leasing"),
            edit_form_filling_leasing(name="edit_leasing"),
            form_filling_no_leasing(name="no_leasing"),
            About_Us(name="about us"),
        ]
        for screen in screens:
            self.sm.add_widget(screen)

        # The app will launch with this screen
        self.sm.current = "welcome"

        # Return the ScreenManager as the root widget
        return self.sm

    # --- Database and Navigation Methods ---

    def on_search(self):
        print("SearchScreen.on_search() called!")

        search_screen = self.sm.get_screen("search")
        search_text = search_screen.ids.search_input.text.strip()
        print(f"SearchScreen.on_search() - Search text retrieved: '{search_text}'")

        results = MDApp.get_running_app().search_pdfs(
            search_text
        )  # method that queries the DB
        print(f"SearchScreen.on_search() - Results from search_pdfs: {results}")

        search_results_list = search_screen.ids.search_results
        print(
            f"SearchScreen.on_search() - search_results_list (MDBoxLayout): {search_results_list}"
        )  # Changed to MDBoxLayout
        search_results_list.clear_widgets()
        print("SearchScreen.on_search() - search_results_list widgets cleared.")

        if results:
            print(
                "SearchScreen.on_search() - Results are NOT empty (if block entered)."
            )
            print("Results:", results)

            for row in results:
                print(f"SearchScreen.on_search() - Processing row: {row}")
                # Create MDGridLayout for each result row to align items horizontally
                result_layout = MDGridLayout(
                    cols=4,
                    spacing=dp(10),
                    size_hint_y=None,
                    height=dp(40),
                    row_default_height=dp(40),
                )  # Adjusted for row height

                # Label for search result
                label_text = (
                    f"{row[0]} - {row[1]} - {row[2]} | {row[3]} - {row[4]} - {row[5]}"
                )
                label = MDLabel(
                    text=label_text,
                    halign="left",
                    theme_text_color="Primary",
                    valign="center",
                    size_hint_y=None,
                    height=dp(40),
                    padding_x=dp(10),
                    shorten=True,  # Enable text shortening
                    shorten_from="right",  # Shorten from right if text is too long
                    # on_touch_down=lambda instance, touch, r=row: self.on_label_click(instance, touch, r)
                )
                result_layout.add_widget(label)
                divider = MDDivider(size_hint_x=1)

                # Edit Button
                edit_button = MDButton(
                    MDButtonText(
                        text="Edit",
                        font_style="Label",
                        role="large",
                    ),
                    style="outlined",  # Added style for visual distinction
                    on_release=lambda _, r=row: self.on_edit_button_click(
                        r
                    ),  # Pass row to button click handler
                )
                result_layout.add_widget(edit_button)

                # View Button (Placeholder)
                view_button = MDButton(
                    MDButtonText(
                        text="View",
                        font_style="Label",
                        role="large",
                    ),
                    style="outlined",  # Added style for visual distinction
                    on_release=lambda _, r=row: self.on_view_button_click(
                        r
                    ),  # Placeholder function
                )
                result_layout.add_widget(view_button)

                # Export Button (Placeholder)
                export_button = MDButton(
                    MDButtonText(
                        text="Export",
                        font_style="Label",
                        role="large",
                    ),
                    style="outlined",  # Added style for visual distinction
                    on_release=lambda _, r=row: self.on_export_button_click(
                        r
                    ),  # Placeholder function
                )
                result_layout.add_widget(export_button)

                search_results_list.add_widget(
                    result_layout
                )  # Add the row layout to the results list
                search_results_list.add_widget(divider)
                print(
                    f"SearchScreen.on_search() - Widget added to list. List children count: {len(search_results_list.children)}"
                )
            print("SearchScreen.on_search() - Widget population loop finished.")
        else:
            print("SearchScreen.on_search() - Results are EMPTY (else block entered).")
            no_results_label = MDLabel(
                text="No results found.", halign="center", theme_text_color="Secondary"
            )
            print(
                f"SearchScreen.on_search() - Created no_results_label: {no_results_label}"
            )
            search_results_list.add_widget(no_results_label)
            print("SearchScreen.on_search() - No results label added to list.")
        print("SearchScreen.on_search() - Method execution finished.")

    def on_search2(self):
        print("SearchScreen.on_search() called!")

        search_screen = self.sm.get_screen("search2")
        search_text = search_screen.ids.search_input.text.strip()
        print(f"SearchScreen.on_search() - Search text retrieved: '{search_text}'")

        results = MDApp.get_running_app().search_pdfs(
            search_text
        )  # method that queries the DB
        print(f"SearchScreen.on_search() - Results from search_pdfs: {results}")

        search_results_list = search_screen.ids.search_results
        print(
            f"SearchScreen.on_search() - search_results_list (MDBoxLayout): {search_results_list}"
        )  # Changed to MDBoxLayout
        search_results_list.clear_widgets()
        print("SearchScreen.on_search() - search_results_list widgets cleared.")

        if results:
            print(
                "SearchScreen.on_search() - Results are NOT empty (if block entered)."
            )
            print("Results:", results)

            for row in results:
                print(f"SearchScreen.on_search() - Processing row: {row}")
                # Create MDGridLayout for each result row to align items horizontally
                result_layout = MDGridLayout(
                    cols=3,
                    spacing=dp(10),
                    size_hint_y=None,
                    height=dp(40),
                    row_default_height=dp(40),
                )  # Adjusted for row height

                # Label for search result
                label_text = (
                    f"{row[0]} - {row[1]} - {row[2]} | {row[3]} - {row[4]} - {row[5]}"
                )
                label = MDLabel(
                    text=label_text,
                    halign="left",
                    theme_text_color="Primary",
                    valign="center",
                    size_hint_y=None,
                    height=dp(40),
                    padding_x=dp(10),
                    shorten=True,  # Enable text shortening
                    shorten_from="right",  # Shorten from right if text is too long
                    # on_touch_down=lambda instance, touch, r=row: self.on_label_click(instance, touch, r)
                )
                result_layout.add_widget(label)
                divider = MDDivider(size_hint_x=1)

                # View Button
                view_button = MDButton(
                    MDButtonText(
                        text="View",
                        font_style="Label",
                        role="large",
                    ),
                    style="outlined",  # Added style for visual distinction
                    on_release=lambda _, r=row: self.on_view_button_click(
                        r
                    ),  # Placeholder function
                )
                result_layout.add_widget(view_button)

                # Export Button
                export_button = MDButton(
                    MDButtonText(
                        text="Export",
                        font_style="Label",
                        role="large",
                    ),
                    style="outlined",  # Added style for visual distinction
                    on_release=lambda _, r=row: self.on_export_button_click(
                        r
                    ),  # Placeholder function
                )
                result_layout.add_widget(export_button)

                search_results_list.add_widget(
                    result_layout
                )  # Add the row layout to the results list
                search_results_list.add_widget(divider)
                print(
                    f"SearchScreen.on_search() - Widget added to list. List children count: {len(search_results_list.children)}"
                )
            print("SearchScreen.on_search() - Widget population loop finished.")
        else:
            print("SearchScreen.on_search() - Results are EMPTY (else block entered).")
            no_results_label = MDLabel(
                text="No results found.", halign="center", theme_text_color="Secondary"
            )
            print(
                f"SearchScreen.on_search() - Created no_results_label: {no_results_label}"
            )
            search_results_list.add_widget(no_results_label)
            print("SearchScreen.on_search() - No results label added to list.")
        print("SearchScreen.on_search() - Method execution finished.")

    def on_edit_button_click(self, file_record):
        """Handles the click event for the Edit button."""
        print(f"Edit Button Clicked - File Record: {file_record}")
        MDApp.get_running_app().edit_file(
            file_record
        )  # Call edit_file with the record the main instance of the app.

    def on_view_button_click(self, file_record):
        """Handles the click event for the View button."""
        print(f"View Button Clicked - File Record: {file_record}")
        pdf_id = file_record[0]
        record_data = self.retrieve_pdf_from_db(pdf_id)
        if record_data:
            # Get the ViewRecordScreen from the ScreenManager
            view_screen = self.sm.get_screen("view_record_screen")
            if view_screen:
                self.display_record(record_data)
                self.nextScreen(
                    "view_record_screen"
                )  # Navigate using nextScreen (for history)
            else:
                self.show_dialog(
                    "Error", "ViewRecordScreen not found in ScreenManager."
                )
        else:
            self.show_dialog("Error", "Could not retrieve record for viewing.")

    def display_record(self, record_data):
        print(f"Record: {record_data}")
        """Populates the ViewRecordScreen with record data - each field on a new line."""
        view_screen = self.sm.get_screen("view_record_screen")
        content_layout = view_screen.ids.content_layout
        content_layout.clear_widgets()

        if not record_data:
            error_label = MDLabel(
                text="Could not retrieve record.",
                theme_text_color="Error",
                halign="center",
            )
            content_layout.add_widget(error_label)
            return

        for key, value in record_data.items():
            # Grid layout for key-value pair
            display_layout = MDGridLayout(
                cols=2,
                spacing=dp(50),
                padding=[dp(50), 0],
                size_hint_y=None,
                height=dp(40),
            )

            key_label = MDLabel(
                text=f"{key.upper()}:",
                font_style="Body",
                halign="left",
                theme_text_color="Primary",
                bold=True,
            )
            value_label = MDLabel(
                text=str(value).upper(),
                font_style="Body",
                theme_text_color="Primary",
                halign="center",
                size_hint_x=None,
                width=dp(150),  # Adjust width as needed
            )

            display_layout.add_widget(key_label)
            display_layout.add_widget(value_label)

            # BoxLayout for divider to take full width
            divider_box = MDBoxLayout(
                size_hint_y=None, height=dp(2)
            )  # Adjust height as needed
            divider = MDDivider(size_hint_x=1)
            divider_box.add_widget(divider)

            content_layout.add_widget(display_layout)
            content_layout.add_widget(divider_box)  # Ensure full-width divider

    # Method that generates the exported pdf
    def generate_pdf(self, file_record):
        """Generates the PDF directly on the main thread."""
        try:
            pdf = CustomPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Prepare data for the table_vertical method.
            data_for_pdf = []
            if isinstance(file_record, dict):
                data_for_pdf.append(file_record)
            elif isinstance(
                file_record, tuple
            ):  # Assuming file_record is a tuple from DB query
                # Convert tuple to dictionary using column names from DB (excluding pdf_data)
                columns = [
                    "id",
                    "pdf_type",
                    "client_name",
                    "locataire",
                    "immat",
                    "last_modified",
                    "version",
                    "object",
                    "cast_type",
                    "serial_number",
                    "doi",
                    "imei",
                    "device_id",
                    "vehicle_type",
                    "chassis",
                    "iccid",
                    "technician_name",
                    "maintenance_opt",
                ]
                file_record_dict = {}
                for i, col_name in enumerate(columns):
                    if i < len(file_record):
                        file_record_dict[col_name] = file_record[i]
                data_for_pdf.append(file_record_dict)

            if not data_for_pdf:
                self.show_dialog(
                    "Error", "No data to display."
                )  # Error dialog on main thread
                return  # Exit if no data

            pdf.table_vertical(data_for_pdf)

            # Use immat for filename, sanitize if needed
            pdf_filename = (
                f"{file_record.get('immat', 'output')}.pdf"
                if isinstance(file_record, dict)
                else f"{file_record[4] if isinstance(file_record, tuple) and len(file_record) > 4 else 'output'}.pdf"
            )  # Get immat from dict or tuple, default to output if immat is not available
            pdf_filename = "".join(
                x for x in pdf_filename if x.isalnum() or x == "."
            ).rstrip()  # Basic sanitization
            pdf_output_path = pdf_filename

            pdf.output(pdf_output_path)
            print(f"PDF generated successfully: {pdf_output_path}")

            # Open the PDF file after creation
            if os.path.exists(pdf_output_path):
                subprocess.Popen([pdf_output_path], shell=True)

            self.show_dialog(
                "Success", f"PDF generated successfully: {pdf_output_path}"
            )  # Success dialog on main thread

        except Exception as e:
            print(f"Error generating PDF: {e}")
            self.show_dialog(
                "Error", f"Error generating PDF: {e}"
            )  # Error dialog on main thread

    def on_export_button_click(self, file_record):
        """Handles the click event for the Export button."""
        print(f"Export Button Clicked - File Record: {file_record}")
        # Call the PDF generation directly (no threading)
        self.generate_pdf(file_record)

    def edit_file(self, file_record):
        try:
            """Handles the file selection from the search results.
            Retrieves the record data and delegates editing based on pdf_type."""
            print(f"edit_file - Received file_record: {file_record}")  # Debug print
            pdf_id, pdf_type = file_record[0], file_record[1]
            print(
                f"edit_file - Extracted PDF ID: {pdf_id}, PDF Type: {pdf_type}"
            )  # Debug print
            extracted_data = self.retrieve_pdf_from_db(
                pdf_id
            )  # Now retrieve_pdf_from_db will exclude pdf_data
            print(
                f"edit_file - Retrieved Data from DB: {extracted_data}"
            )  # Debug print
            if not extracted_data:
                self.show_dialog("Error", "Failed to retrieve file data.")
                return

            if pdf_type.lower() == "leasing":
                self.edit_leasing(extracted_data)
            elif pdf_type.lower() == "no-leasing":
                self.edit_no_leasing(extracted_data)
            else:
                self.show_dialog("Error", "Unknown file type.")
        except Exception as e:
            self.show_dialog("Error", f"{e} occured")

    def retrieve_pdf_from_db(self, pdf_id):
        try:
            print(f"retrieve_pdf_from_db - PDF ID: {pdf_id}")  # Debug print
            cursor = self.conn.cursor()

            # Get column names from the table schema
            cursor.execute("PRAGMA table_info(archives)")
            columns_info = cursor.fetchall()
            all_columns = [col[1] for col in columns_info]

            # Create a list of columns to select, explicitly excluding 'pdf_data'
            columns_to_select = []
            for col in all_columns:
                if col.lower() != "pdf_data":
                    columns_to_select.append(col)

            # Construct the SELECT query to exclude pdf_data
            select_query = (
                f"SELECT {', '.join(columns_to_select)} FROM archives WHERE id = ?"
            )

            cursor.execute(select_query, (pdf_id,))
            row = cursor.fetchone()
            print(f"retrieve_pdf_from_db - Query Result Row: {row}")  # Debug print
            if row:
                # Convert row to a dictionary for easier handling, using filtered columns
                data = {}
                for i, col_name in enumerate(columns_to_select):
                    data[col_name] = row[i]
                print(
                    f"retrieve_pdf_from_db - Data Dictionary (excluding pdf_data): {data}"
                )  # Debug print
                return data
            print("retrieve_pdf_from_db - No Row Found")  # Debug print
            return None
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def search_pdfs(self, search_text):
        cursor = self.conn.cursor()

        # Get column names from the table schema
        cursor.execute("PRAGMA table_info(archives)")
        columns_info = cursor.fetchall()
        all_columns = [col[1] for col in columns_info]

        # Create a list of columns to select, explicitly excluding 'pdf_data'
        columns_to_select = []
        for col in all_columns:
            if col.lower() != "pdf_data":
                columns_to_select.append(col)

        # Construct the SELECT query with specific columns
        select_query = f"SELECT {', '.join(columns_to_select)} FROM archives WHERE client_name LIKE ? OR pdf_type LIKE ? OR locataire LIKE ? OR immat LIKE ? OR CAST(id AS TEXT) LIKE ? ORDER BY last_modified DESC"

        param = f"%{search_text}%"
        cursor.execute(
            select_query, (param, param, param, param, param)
        )  # corrected line
        results = cursor.fetchall()
        return results

    # --- Editing Methods ---
    def edit_leasing(self, extracted_data: dict):
        try:
            fields = [
                "Object:",
                "Locataire:",
                "Cast Type:",
                "Serial Number:",
                "DOI:",
                "IMEI:",
                "Device ID:",
                "Client Name:",
                "Vehicle Type:",
                "IMMAT:",
                "Chassis:",
                "ICCID:",
                "Technician Name:",
            ]

            print(
                f"edit_leasing - Extracted Data Received: {extracted_data}"
            )  # Debug print
            leasing_screen = self.root.get_screen("edit_leasing")
            leasing_screen.pdf_id = extracted_data.get("id")
            leasing_screen.ids.leasing_form.clear_widgets()

            # Create a single form layout
            form_layout = MDBoxLayout(
                orientation="vertical", size_hint_y=None, spacing=dp(10)
            )
            form_layout.bind(minimum_height=form_layout.setter("height"))

            # Create checkbox layout
            checkbox_layout = GridLayout(
                cols=2,
                size_hint_y=None,
                spacing=dp(10),
                height=dp(40 * len(MAINTENANCE_OPTIONS)),
            )
            checkbox_layout.bind(minimum_height=checkbox_layout.setter("height"))

            self.checkboxes = []
            for option in MAINTENANCE_OPTIONS:
                checkbox_item = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )
                checkbox = MDCheckbox(
                    size_hint_x=None, width=dp(40), active=False, disabled=True
                )
                checkbox_item.add_widget(checkbox)
                self.checkboxes.append(checkbox)
                label = MDLabel(
                    text=option,
                    halign="left",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="Body",
                    role="large",
                    size_hint_x=0.6,
                )
                checkbox_item.add_widget(label)
                checkbox_layout.add_widget(checkbox_item)

            # Create a dictionary mapping old keys to new keys
            key_mapping = {
                "object": "Object",
                "locataire": "Locataire",
                "cast_type": "Cast Type",
                "serial_number": "Serial Number",
                "doi": "DOI",
                "imei": "IMEI",
                "device_id": "Device ID",
                "client_name": "Client Name",
                "vehicle_type": "Vehicle Type",
                "immat": "IMMAT",
                "chassis": "Chassis",
                "iccid": "ICCID",
                "technician_name": "Technician Name",
                "maintenance_opt": "Maintenance_opt",
            }

            # Use dictionary comprehension to create a new dictionary with the new keys
            extracted_data = {
                key_mapping[key]: value
                for key, value in extracted_data.items()
                if key in key_mapping
            }

            print("New Extracted data: ", extracted_data)
            # Enable checkboxes if the Object field indicates maintenance
            if extracted_data.get("Object") == "MAINTENANCE":
                for i, option in enumerate(MAINTENANCE_OPTIONS):
                    if option in extracted_data.get("Maintenance_opt", "").split(", "):
                        self.checkboxes[i].active = True
                        self.checkboxes[i].disabled = False
                    else:
                        self.checkboxes[i].active = False
                        self.checkboxes[i].disabled = False

            form_layout.add_widget(checkbox_layout)

            for field in fields:
                field_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )
                field_label = MDLabel(
                    text=field,
                    size_hint_x=0.3,
                    halign="center",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="Title",
                    role="large",
                )
                field_layout.add_widget(field_label)

                if field == "Object:":
                    dropdown_button = MDButton(
                        MDButtonText(
                            text=extracted_data.get(field[:-1], "Select Object"),
                            theme_text_color="Custom",
                            text_color=(0, 0, 0, 1),
                        ),
                        size_hint=(0.4, None),
                        height=dp(40),
                    )
                    menu_items = [
                        {
                            "text": obj,
                            "on_release": lambda x=obj, btn=dropdown_button: self.set_object(
                                btn, x, None, self.checkboxes
                            ),
                            "theme_text_color": "Custom",
                            "text_color": (198 / 255.0, 57 / 255.0, 57 / 255.0, 1),
                        }
                        for obj in OBJECTS
                    ]
                    dropdown_menu = MDDropdownMenu(
                        caller=dropdown_button, items=menu_items, width_mult=4
                    )
                    dropdown_button.bind(
                        on_release=lambda btn=dropdown_button: dropdown_menu.open()
                    )
                    field_layout.add_widget(dropdown_button)
                else:
                    field_input = TextInput(
                        text=extracted_data.get(field[:-1], ""),
                        multiline=False,
                        size_hint_x=0.7,
                        height=dp(30),
                    )
                    field_layout.add_widget(field_input)
                form_layout.add_widget(field_layout)

            leasing_screen.ids.leasing_form.add_widget(form_layout)
            self.nextScreen("edit_leasing")
        except Exception as e:
            print(f"Error during edit_leasing: {e}")
            self.show_dialog("Error", f"Failed to load leasing edit form: {e}")

    def save_leasing_edit(self, pdf_id):
        """Saves edits made in the edit_leasing form to the database for an existing record."""
        edit_leasing_screen = self.root.get_screen(
            "edit_leasing"
        )  # Correct screen name

        # Extract data from form fields - similar to save_no_leasing_pdf
        form = edit_leasing_screen.ids.leasing_form.children[
            0
        ]  # Assuming form_layout is the first child
        data: dict = {}
        maintenance_selections: list = []

        fields = [
            "Object",
            "Locataire",
            "Maintenance_opt",
            "Cast Type",
            "Serial Number",
            "DOI",
            "IMEI",
            "Device ID",
            "Client Name",
            "Vehicle Type",
            "IMMAT",
            "Chassis",
            "ICCID",
            "Technician Name",
        ]

        for field_layout in form.children:
            if isinstance(field_layout, MDBoxLayout) and len(field_layout.children) > 1:
                label = field_layout.children[1]
                input_field = field_layout.children[0]

                if isinstance(input_field, TextInput):
                    field_name = label.text[:-1]
                    data[field_name] = input_field.text.upper()
                elif isinstance(input_field, MDButton):  # Dropdown button
                    field_name = label.text[:-1]
                    data[field_name] = input_field.children[0].text
            elif isinstance(field_layout, GridLayout):  # Checkboxes
                for checkbox_item in field_layout.children:
                    checkbox = checkbox_item.children[1]
                    label = checkbox_item.children[0].text
                    if checkbox.active:
                        maintenance_selections.append(label)

        data["Maintenance_opt"] = ", ".join(maintenance_selections)

        # Get metadata for the archive entry
        client_name = data.get("Client Name", "Unknown_Client")
        locataire = data.get("Locataire", "Unknown_Locataire")
        immat = data.get("IMMAT", "Unknown_IMMAT")
        objet = data.get("Object", "")
        cast_type = data.get("Cast Type", "")
        serial_num = data.get("Serial Number", "")
        doi = data.get("DOI", "")
        imei = data.get("IMEI", "")
        device_id = data.get("Device ID", "")
        vehicle_type = data.get("Vehicle Type", "")
        chassis = data.get("Chassis", "")
        iccid = data.get("ICCID", "")
        technician_name = data.get("Technician Name", "")

        maintenance_opt = data.get("Maintenance_opt")

        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE archives
                SET client_name = ?, locataire = ?, immat = ?,
                    `object` = ?, `cast_type` = ?, `serial_number` = ?,
                    `doi` = ?, `imei` = ?, `device_id` = ?, `vehicle_type` = ?,
                    `chassis` = ?, `iccid` = ?, `technician_name` = ?,
                    `maintenance_opt` = ?,
                    last_modified = CURRENT_TIMESTAMP, version = version + 1
                WHERE id = ?
            """
            cursor.execute(
                query,
                (
                    client_name,
                    locataire,
                    immat,
                    objet,
                    cast_type,
                    serial_num,
                    doi,
                    imei,
                    device_id,
                    vehicle_type,
                    chassis,
                    iccid,
                    technician_name,
                    maintenance_opt,
                    pdf_id,  # WHERE clause condition - pdf_id
                ),
            )
            self.conn.commit()
            print(
                f"Leasing PDF record updated in database for ID: {pdf_id}, client: {client_name}, immat: {immat}"
            )
            self.show_dialog(
                "Success", "Record updated successfully!"
            )  # General success message for update
        except Exception as e:
            print(f"Error updating leasing PDF record in database: {e}")
            self.show_dialog(
                "Error", f"Failed to update record: {e}"
            )  # General error message for update

    def edit_no_leasing(self, extracted_data: dict):
        try:
            fields = [
                "Object:",
                "Cast Type:",
                "Serial Number:",
                "DOI:",
                "IMEI:",
                "Device ID:",
                "Client Name:",
                "Vehicle Type:",
                "IMMAT:",
                "Chassis:",
                "ICCID:",
                "Technician Name:",
            ]

            print(
                f"edit_no_leasing - Extracted Data Received: {extracted_data}"
            )  # Debug print
            no_leasing_screen = self.root.get_screen("edit_no_leasing")
            no_leasing_screen.pdf_id = extracted_data.get("id")
            no_leasing_screen.ids.no_leasing_form.clear_widgets()

            # Create a single form layout
            form_layout = MDBoxLayout(
                orientation="vertical", size_hint_y=None, spacing=dp(10)
            )
            form_layout.bind(minimum_height=form_layout.setter("height"))

            # Create checkbox layout
            checkbox_layout = GridLayout(
                cols=2,
                size_hint_y=None,
                spacing=dp(10),
                height=dp(40 * len(MAINTENANCE_OPTIONS)),
            )
            checkbox_layout.bind(minimum_height=checkbox_layout.setter("height"))

            self.checkboxes = []
            for option in MAINTENANCE_OPTIONS:
                checkbox_item = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )
                checkbox = MDCheckbox(
                    size_hint_x=None, width=dp(40), active=False, disabled=True
                )
                checkbox_item.add_widget(checkbox)
                self.checkboxes.append(checkbox)
                label = MDLabel(
                    text=option,
                    halign="left",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="Body",
                    role="large",
                    size_hint_x=0.6,
                )
                checkbox_item.add_widget(label)
                checkbox_layout.add_widget(checkbox_item)

            # Create a dictionary mapping old keys to new keys
            key_mapping = {
                "object": "Object",
                "cast_type": "Cast Type",
                "serial_number": "Serial Number",
                "doi": "DOI",
                "imei": "IMEI",
                "device_id": "Device ID",
                "client_name": "Client Name",
                "vehicle_type": "Vehicle Type",
                "immat": "IMMAT",
                "chassis": "Chassis",
                "iccid": "ICCID",
                "technician_name": "Technician Name",
                "maintenance_opt": "Maintenance_opt",
            }

            # Use dictionary comprehension to create a new dictionary with the new keys
            extracted_data = {
                key_mapping[key]: value
                for key, value in extracted_data.items()
                if key in key_mapping
            }

            print("New Extracted data: ", extracted_data)
            # Enable checkboxes if "Object" is "MAINTENANCE"
            if extracted_data.get("Object") == "MAINTENANCE":
                for i, option in enumerate(MAINTENANCE_OPTIONS):
                    if option in extracted_data.get("Maintenance_opt", "").split(", "):
                        self.checkboxes[i].active = True
                        self.checkboxes[i].disabled = False
                    else:
                        self.checkboxes[i].active = False
                        self.checkboxes[i].disabled = False

            form_layout.add_widget(checkbox_layout)

            for field in fields:
                field_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )
                field_label = MDLabel(
                    text=field,
                    size_hint_x=0.3,
                    halign="center",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="Title",
                    role="large",
                )
                field_layout.add_widget(field_label)

                if field == "Object:":
                    dropdown_button = MDButton(
                        MDButtonText(
                            text=extracted_data.get(field[:-1], "Select Object"),
                            theme_text_color="Custom",
                            text_color=(0, 0, 0, 1),
                        ),
                        size_hint=(0.4, None),
                        height=dp(40),
                    )
                    menu_items = [
                        {
                            "text": obj,
                            "on_release": lambda x=obj, btn=dropdown_button: self.set_object(
                                btn, x, None, self.checkboxes
                            ),
                            "theme_text_color": "Custom",
                            "text_color": (198 / 255.0, 57 / 255.0, 57 / 255.0, 1),
                        }
                        for obj in OBJECTS
                    ]
                    dropdown_menu = MDDropdownMenu(
                        caller=dropdown_button, items=menu_items, width_mult=4
                    )
                    dropdown_button.bind(
                        on_release=lambda btn=dropdown_button: dropdown_menu.open()
                    )
                    field_layout.add_widget(dropdown_button)
                else:
                    field_input = TextInput(
                        text=extracted_data.get(field[:-1], ""),
                        multiline=False,
                        size_hint_x=0.7,
                        height=dp(30),
                    )
                    field_layout.add_widget(field_input)
                form_layout.add_widget(field_layout)

            no_leasing_screen.ids.no_leasing_form.add_widget(form_layout)
            self.nextScreen("edit_no_leasing")
        except Exception as e:
            print(f"Error during edit_no_leasing: {e}")
            self.show_dialog("Error", f"Failed to load no-leasing edit form: {e}")

    def save_no_leasing_edit(self, pdf_id):
        """Saves edits made in the edit_no_leasing form to the database for an existing record."""
        edit_no_leasing_screen = self.root.get_screen(
            "edit_no_leasing"
        )  # Correct screen name

        # Extract data from form fields - similar to save_no_leasing_pdf
        form = edit_no_leasing_screen.ids.no_leasing_form.children[
            0
        ]  # Assuming form_layout is the first child
        data: dict = {}
        maintenance_selections: list = []

        fields = [
            "Object",
            "Maintenance_opt",
            "Cast Type",
            "Serial Number",
            "DOI",
            "IMEI",
            "Device ID",
            "Client Name",
            "Vehicle Type",
            "IMMAT",
            "Chassis",
            "ICCID",
            "Technician Name",
        ]

        for field_layout in form.children:
            if isinstance(field_layout, MDBoxLayout) and len(field_layout.children) > 1:
                label = field_layout.children[1]
                input_field = field_layout.children[0]

                if isinstance(input_field, TextInput):
                    field_name = label.text[:-1]
                    data[field_name] = input_field.text.upper()
                elif isinstance(input_field, MDButton):  # Dropdown button
                    field_name = label.text[:-1]
                    data[field_name] = input_field.children[0].text
            elif isinstance(field_layout, GridLayout):  # Checkboxes
                for checkbox_item in field_layout.children:
                    checkbox = checkbox_item.children[1]
                    label = checkbox_item.children[0].text
                    if checkbox.active:
                        maintenance_selections.append(label)

        data["Maintenance_opt"] = ", ".join(maintenance_selections)

        # Get metadata for the archive entry
        client_name = data.get("Client Name", "Unknown_Client")
        locataire = data.get("Locataire", "Unknown_Locataire")
        immat = data.get("IMMAT", "Unknown_IMMAT")
        objet = data.get("Object", "")
        cast_type = data.get("Cast Type", "")
        serial_num = data.get("Serial Number", "")
        doi = data.get("DOI", "")
        imei = data.get("IMEI", "")
        device_id = data.get("Device ID", "")
        vehicle_type = data.get("Vehicle Type", "")
        chassis = data.get("Chassis", "")
        iccid = data.get("ICCID", "")
        technician_name = data.get("Technician Name", "")

        maintenance_opt = data.get("Maintenance_opt")

        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE archives
                SET client_name = ?, locataire = ?, immat = ?,
                    `object` = ?, `cast_type` = ?, `serial_number` = ?,
                    `doi` = ?, `imei` = ?, `device_id` = ?, `vehicle_type` = ?,
                    `chassis` = ?, `iccid` = ?, `technician_name` = ?,
                    `maintenance_opt` = ?,
                    last_modified = CURRENT_TIMESTAMP, version = version + 1
                WHERE id = ?
            """
            cursor.execute(
                query,
                (
                    client_name,
                    None,
                    immat,
                    objet,
                    cast_type,
                    serial_num,
                    doi,
                    imei,
                    device_id,
                    vehicle_type,
                    chassis,
                    iccid,
                    technician_name,
                    maintenance_opt,
                    pdf_id,  # WHERE clause condition - pdf_id
                ),
            )
            self.conn.commit()
            print(
                f"No-Leasing PDF record updated in database for ID: {pdf_id}, client: {client_name}, immat: {immat}"
            )
            self.show_dialog(
                "Success", "Record updated successfully!"
            )  # General success message for update
        except Exception as e:
            print(f"Error updating no-leasing PDF record in database: {e}")
            self.show_dialog(
                "Error", f"Failed to update record: {e}"
            )  # General error message for update

    def show_add_account_dialog(self):
        self.add_dialog = None

        if not self.add_dialog:
            # Create an Image widget and set the source (path to your image)
            content_grid = MDGridLayout(
                cols=2, spacing=20, padding=20, size_hint_y=None, id="content_grid"
            )  # Assign id to content_grid, rename to content_grid for clarity
            content_grid.height = dp(250)
            username = MDTextField(
                MDTextFieldHintText(text="Username"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
            )

            password = MDTextField(
                MDTextFieldHintText(text="Password"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
                password=True,
            )

            role = MDTextField(
                MDTextFieldHintText(text="Role"),
                MDTextFieldTrailingIcon(icon="eye-off"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
            )

            admin_password = MDTextField(
                MDTextFieldHintText(text="Admin Password"),
                MDTextFieldTrailingIcon(icon="eye-off"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
                password=True,
            )

            error_label = MDLabel(
                id="update_error_label_dialog",  # Assign id to error_label
                text="",
                theme_text_color="Custom",
                text_color=(0.9, 0.1, 0.1, 1),
                halign="center",
            )

            content_grid.add_widget(username)
            content_grid.add_widget(role)
            content_grid.add_widget(password)
            content_grid.add_widget(admin_password)
            content_grid.add_widget(error_label)

            cancel_button = MDButton(
                MDButtonText(
                    text="Cancel",
                    font_style="Label",
                    role="large",
                ),
                on_release=lambda x: self.add_dialog.dismiss(),
            )

            update_button = MDButton(
                MDButtonText(
                    text="Update",
                    font_style="Label",
                    role="large",
                ),
                on_release=lambda x: self.create_account_db_from_dialog(
                    username.text,
                    password.text,
                    role.text,
                    admin_password.text,
                    error_label,
                ),
            )

            self.add_dialog = MDDialog(
                MDDialogHeadlineText(
                    text="Create User Account",
                    halign="left",
                ),
                MDDialogContentContainer(
                    content_grid,  # Use content_grid here
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    cancel_button,
                    # Widget(),
                    update_button,
                    spacing=dp(10),
                ),
                auto_dismiss=False,
                size_hint=(None, None),
                width=dp(720),
                height=dp(200),
                radius=[dp(8), dp(8), dp(8), dp(8)],
            )
            self.add_dialog.open()

    def show_delete_account_dialog(self):
        self.delete_dialog = None

        if not self.delete_dialog:
            content_grid = MDBoxLayout(
                orientation="vertical",
                spacing=55,
                padding=10,
                size_hint_y=None,
                id="content_grid",
            )  # Assign id to content_grid, rename to content_grid for clarity
            content_grid.height = dp(250)
            username = MDTextField(
                MDTextFieldHintText(text="Username"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
            )

            admin_password = MDTextField(
                MDTextFieldHintText(text="Admin Password"),
                MDTextFieldTrailingIcon(icon="eye-off"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
                password=True,
            )

            error_label = MDLabel(
                id="update_error_label_dialog",  # Assign id to error_label
                text="",
                theme_text_color="Custom",
                text_color=(0.9, 0.1, 0.1, 1),
                halign="center",
            )

            content_grid.add_widget(username)
            content_grid.add_widget(admin_password)
            content_grid.add_widget(error_label)

            cancel_button = MDButton(
                MDButtonText(
                    text="Cancel",
                    font_style="Label",
                    role="large",
                ),
                on_release=lambda x: self.delete_dialog.dismiss(),
            )

            update_button = MDButton(
                MDButtonText(
                    text="Update",
                    font_style="Label",
                    role="large",
                ),
                on_release=lambda x: self.delete_account_db_from_dialog(
                    username.text, admin_password.text, error_label
                ),
            )

            self.delete_dialog = MDDialog(
                MDDialogHeadlineText(
                    text="Delete User Account",
                    halign="left",
                ),
                MDDialogContentContainer(
                    content_grid,  # Use content_grid here
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    cancel_button,
                    # Widget(),
                    update_button,
                    spacing=dp(10),
                ),
                auto_dismiss=False,
                size_hint=(0.7, 0.5),
                # width = dp(720),
                # height=dp(200),
                radius=[dp(8), dp(8), dp(8), dp(8)],
            )
            self.delete_dialog.open()

    def show_update_account_dialog(self):
        self.update_dialog = None

        if not self.update_dialog:
            content_grid = MDGridLayout(
                cols=2, spacing=20, padding=20, size_hint_y=None, id="content_grid"
            )  # Assign id to content_grid, rename to content_grid for clarity
            content_grid.height = dp(250)
            username = MDTextField(
                MDTextFieldHintText(text="Username"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
            )

            new_role = MDTextField(
                MDTextFieldHintText(text="Role"),
                MDTextFieldTrailingIcon(icon="eye-off"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
            )

            admin_password = MDTextField(
                MDTextFieldHintText(text="Admin Password"),
                MDTextFieldTrailingIcon(icon="eye-off"),
                MDTextFieldMaxLengthText(max_text_length=7),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
                password=True,
            )

            error_label = MDLabel(
                id="update_error_label_dialog",  # Assign id to error_label
                text="",
                theme_text_color="Custom",
                text_color=(0.9, 0.1, 0.1, 1),
                halign="center",
            )

            content_grid.add_widget(username)
            content_grid.add_widget(new_role)
            content_grid.add_widget(admin_password)
            content_grid.add_widget(error_label)

            cancel_button = MDButton(
                MDButtonText(
                    text="Cancel",
                    font_style="Label",
                    role="large",
                ),
                on_release=lambda x: self.update_dialog.dismiss(),
            )

            update_button = MDButton(
                MDButtonText(
                    text="Update",
                    font_style="Label",
                    role="large",
                ),
                on_release=lambda x: self.update_account_db_from_dialog(
                    username.text, new_role.text, admin_password.text, error_label
                ),
            )

            self.update_dialog = MDDialog(
                MDDialogHeadlineText(
                    text="Change User Role",
                    halign="left",
                ),
                MDDialogContentContainer(
                    content_grid,  # Use content_grid here
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    cancel_button,
                    # Widget(),
                    update_button,
                    spacing=dp(10),
                ),
                auto_dismiss=False,
                size_hint=(None, None),
                width=dp(720),
                height=dp(200),
                radius=[dp(8), dp(8), dp(8), dp(8)],
            )
            self.update_dialog.open()

    def delete_account_db_from_dialog(
        self, username_to_delete, admin_password, error_label
    ):  # Added error_label parameter
        """Deletes a user account after validating admin password and verifying deletion."""

        if not username_to_delete or not admin_password:
            error_label.text = "All fields are required."
            return

        try:
            cursor = self.conn.cursor()
            # --- VALIDATE ADMIN PASSWORD ---
            cursor.execute(
                "SELECT 1 FROM users WHERE role = 'admin' AND password = ?",
                (admin_password,),
            )
            admin_user_exists = cursor.fetchone()

            if admin_user_exists:
                # --- Get initial row count ---
                cursor.execute("SELECT COUNT(*) FROM users")
                initial_row_count = cursor.fetchone()[0]

                # --- DELETE USER ACCOUNT ---
                cursor.execute(
                    "DELETE FROM users WHERE user_name = ?", (username_to_delete,)
                )
                self.conn.commit()

                # --- Get final row count ---
                cursor.execute("SELECT COUNT(*) FROM users")
                final_row_count = cursor.fetchone()[0]

                if final_row_count < initial_row_count:  # Check if row count decreased
                    error_label.text = "Account deleted successfully!"
                    error_label.text_color = "green"
                    Clock.schedule_once(
                        lambda dt: self.delete_dialog.dismiss(), 1
                    )  # Close after 1 seconds
                else:
                    error_label.text = "Username not found or deletion failed."  # User not found or delete failed (though DELETE usually succeeds even if user not found, rowcount would be 0)

            else:
                error_label.text = "Incorrect Admin Password."

        except sqlite3.Error as e:
            print(f"Database error deleting account: {e}")
            error_label.text = f"Database Error: {e}"

    def create_account_db_from_dialog(
        self, username, password, role, admin_password, error_label
    ):
        """Creates a new user account after validating admin password against DB."""

        if not username or not password or not role or not admin_password:
            error_label.text = "All fields are required."
            return

        valid_roles = ["admin", "editor", "viewer"]
        if role not in valid_roles:
            error_label.text = "Invalid role. Must be admin, editor, or viewer."
            return

        try:
            cursor = self.conn.cursor()
            # --- VALIDATE ADMIN PASSWORD AGAINST DATABASE ---
            """"""
            cursor.execute(
                "SELECT 1 FROM users WHERE role = 'admin' AND password = ?",
                (admin_password,),
            )
            admin_user_exists = cursor.fetchone()  # Fetch one row, if admin exists

            if admin_user_exists:  # Admin password is valid (admin user found)
                # --- Get initial row count ---
                cursor.execute("SELECT COUNT(*) FROM users")
                initial_row_count = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO users (user_name, password, role) VALUES (?, ?, ?)
                """,
                    (username, password, role),
                )
                self.conn.commit()

                # --- Get final row count ---
                cursor.execute("SELECT COUNT(*) FROM users")
                final_row_count = cursor.fetchone()[0]

                if final_row_count > initial_row_count:
                    error_label.text = "Account created successfully!"
                    error_label.text_color = "green"
                    Clock.schedule_once(
                        lambda dt: self.add_dialog.dismiss(), 1
                    )  # Close after 1 seconds
                else:
                    error_label.text = "Username already exists."
            else:
                error_label.text = "Incorrect Admin Password."  # Admin password invalid

        except sqlite3.Error as e:
            print(f"Database error creating account: {e}")
            error_label.text = f"Database Error: {e}"

    def update_account_db_from_dialog(
        self,
        username_to_update: str,
        new_role: str,
        admin_password: str,
        error_label: MDLabel,
    ) -> None:
        """Updates a user account's role after validating admin password and verifying update."""

        if not username_to_update or not new_role or not admin_password:
            error_label.text = "All fields are required."
            return

        valid_roles = ["admin", "editor", "viewer"]
        if new_role not in valid_roles:
            error_label.text = "Invalid role. Must be admin, editor, or viewer."
            return

        try:
            cursor = self.conn.cursor()
            # --- VALIDATE ADMIN PASSWORD ---
            cursor.execute(
                "SELECT 1 FROM users WHERE role = 'admin' AND password = ?",
                (admin_password,),
            )
            admin_user_exists = cursor.fetchone()

            if admin_user_exists:
                # --- Get initial row count (number of users with the username to update, should be 0 or 1) ---
                cursor.execute(
                    "SELECT COUNT(*) FROM users WHERE user_name = ?",
                    (username_to_update,),
                )
                initial_affected_row_count = cursor.fetchone()[
                    0
                ]  # How many rows *before* update

                # --- UPDATE USER ROLE ---
                cursor.execute(
                    "UPDATE users SET role = ? WHERE user_name = ?",
                    (new_role, username_to_update),
                )
                self.conn.commit()

                # --- Get final affected row count (should still be 0 or 1, and ideally unchanged if username existed) ---
                cursor.execute(
                    "SELECT changes() FROM sqlite_master"
                )  # sqlite_master table doesn't exist, should be cursor.execute("SELECT changes()")
                final_affected_row_count = cursor.fetchone()[
                    0
                ]  # How many rows *were* changed by UPDATE

                if (
                    final_affected_row_count > 0
                ):  # Check if any rows were actually updated
                    error_label.text = "Account role updated successfully!"
                    error_label.text_color = "green"
                    Clock.schedule_once(
                        lambda dt: self.update_dialog.dismiss(), 1
                    )  # Close after 1 seconds
                else:
                    error_label.text = "Username not found or update failed."  # Username not found or update failed (if username existed but role update somehow failed, though UPDATE usually succeeds even if role is the same)

            else:
                error_label.text = "Incorrect Admin Password."

        except sqlite3.Error as e:
            print(f"Database error updating account role: {e}")
            error_label.text = f"Database Error: {e}"

    def dialog_box(self):
        self.dialog = None

        # Check if self.dialog is empty ie it is False
        if not self.dialog:
            # Create a custom layout for the dialog using GridLayout for better alignment
            content_layout = GridLayout(
                cols=3, padding=10, spacing=10, size_hint_y=None
            )
            content_layout.height = dp(200)

            # Dictionary to store the user input for each row and checkbox states
            self.file_inputs = {}
            self.checkbox_states = {}

            # Function to handle checkbox state change and ensure only one checkbox is selected
            # This function is not an instance method because it is found inside an instance method
            # For it to be an instance method it should be used outside the dialog_box method directly inside the class
            # Otherwise trying to call it both using 'self' and outside the dialog_box method would lead to an AttributeError
            def on_checkbox_active(checkbox, value, file_input, opposite_checkbox):
                if value:
                    opposite_checkbox.active = False  # Deactivate the other checkbox
                    file_input.disabled = (
                        False  # Enable TextInput when checkbox is active
                    )
                else:
                    file_input.disabled = (
                        True  # Disable TextInput when checkbox is inactive
                    )
                    file_input.text = ""  # Clear the text if unchecked

                self.check_submit_button_state()  # Check if submit button can be enabled or not based on the required conditions

            # Row 1: Checkbox for "Yes", Label "Yes", and TextInput for "No of files"
            yes_checkbox = MDCheckbox(size_hint=(0.2, None), height=dp(40))
            content_layout.add_widget(yes_checkbox)  # Adds the yes_checkbox
            content_layout.add_widget(MDLabel(text="Yes", size_hint_x=0.3))
            file_input_yes = MDTextField(
                MDTextFieldHintText(text="Enter number of files"),
                MDTextFieldHelperText(text="Too many files"),
                MDTextFieldMaxLengthText(max_text_length=2),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
                input_filter="int",
                disabled="True",
            )
            self.file_inputs["yes"] = file_input_yes
            self.checkbox_states["yes"] = yes_checkbox
            content_layout.add_widget(file_input_yes)  # Adds the textinput

            # Row 2: Checkbox for "No", Label "No", and TextInput for "No of files"
            no_checkbox = MDCheckbox(size_hint=(0.2, None), height=dp(40))
            content_layout.add_widget(no_checkbox)  # Adds the no_checkbox
            content_layout.add_widget(MDLabel(text="No", size_hint_x=0.3))
            file_input_no = MDTextField(
                MDTextFieldHintText(text="Enter number of files"),
                MDTextFieldTrailingIcon(icon="information"),
                MDTextFieldMaxLengthText(max_text_length=2),
                mode="filled",
                size_hint_x=None,
                width=dp(300),
                theme_line_color="Custom",
                line_color_normal="green",
                line_color_focus="blue",
                input_filter="int",
                disabled="True",
            )
            self.file_inputs["no"] = file_input_no
            self.checkbox_states["no"] = no_checkbox
            content_layout.add_widget(file_input_no)  # Adds the textinput

            # Ensure only one checkbox can be checked at a time
            yes_checkbox.bind(
                active=lambda checkbox, value: on_checkbox_active(
                    checkbox, value, file_input_yes, no_checkbox
                )
            )
            no_checkbox.bind(
                active=lambda checkbox, value: on_checkbox_active(
                    checkbox, value, file_input_no, yes_checkbox
                )
            )

            # Bind TextInput changes to enable/disable submit button
            file_input_yes.bind(
                text=lambda textinput, value: self.check_submit_button_state()
            )
            # The self.check_submit_button_state() method is call to check whether the submit button should be enable or not
            file_input_no.bind(
                text=lambda textinput, value: self.check_submit_button_state()
            )

            # Create the action button that will gather the data
            self.confirm_button = MDButton(
                MDButtonText(
                    text="Submit",
                    font_style="Body",
                    role="large",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                # style="outlined",
                # theme_line_color="Custom",
                # theme_bg_color="Custom",
                # md_bg_color=(0.9, 0.9, 0.9, 0.5),
                # line_color="blue",
                on_press=self.on_confirm,
                # disabled=True  # Initially
                opacity=0,
            )
            # content_layout.add_widget(self.confirm_button)  # Adds the submit button to the screen

            # Create the dialog box
            self.dialog = MDDialog(
                MDDialogHeadlineText(
                    text="Leasing Condition",
                    halign="left",
                ),
                MDDialogContentContainer(
                    content_layout,
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    self.confirm_button,
                ),
                size_hint=(0.6, None),
                height=dp(200),
                scrim_color=(1, 1, 1, 1),
                radius=[dp(8), dp(8), dp(8), dp(8)],
            )
        self.dialog.open()

    def check_submit_button_state(self):
        # Check if either checkbox is selected and the corresponding TextInput is filled
        if (self.checkbox_states["yes"].active and self.file_inputs["yes"].text) or (
            self.checkbox_states["no"].active and self.file_inputs["no"].text
        ):  # \ is used in this context as a line continuation character
            self.confirm_button.opacity = 1  # display the submit button
        else:
            self.confirm_button.opacity = 0  # hide the submit button

    def on_confirm(self, obj):
        selected_info = []  # NOT BEEN USED

        yes_selected = self.checkbox_states["yes"].active
        yes_files = self.file_inputs["yes"].text or "0"
        # self.number_times_yes = yes_files # Not been used
        selected_info.append(
            f"Yes: {yes_files} files {'selected' if yes_selected else 'not selected'}"
        )

        no_selected = self.checkbox_states["no"].active
        no_files = self.file_inputs["no"].text or "0"
        # self.number_times_no = no_files # Not been used
        selected_info.append(
            f"No: {no_files} files {'selected' if no_selected else 'not selected'}"
        )

        # Used to concatenate all the string values inside selected_info list as one string splitting them into 2 lines
        # print("\n".join(selected_info))
        self.dialog.dismiss()

        if yes_selected:  # If the 'Yes' checkbox was checked ie active
            # self.root.current = "leasing"
            self.leasing_yes(yes_files)
            print("Leasing Screen")
            print("Submit button clicked")
            print("Checkbox states:", self.checkbox_states)
            print("File inputs:", self.file_inputs)
            self.nextScreen("leasing")
        elif no_selected:  # If the 'No' checkbox was checked ie active
            # self.root.current = "no_leasing"
            self.leasing_no(no_files)
            print("No_Leasing Screen")
            print("Submit button clicked")
            print("Checkbox states:", self.checkbox_states)
            print("File inputs:", self.file_inputs)
            self.nextScreen("no_leasing")

    # Method used to create and manage the form for leasing vehicles
    def leasing_yes(self, times):
        times = int(times)
        leasing_screen = self.root.get_screen("leasing")

        # Clear any existing widgets before adding new ones
        leasing_screen.ids.leasing_form.clear_widgets()

        # Store the different dropdown_menus
        self.dropdown_menus = {}
        self.forms = []  # Store the forms

        # Iterate for the number of times specified by the user
        for i in range(times):
            # Create a new vertical BoxLayout for the form
            form_layout = MDBoxLayout(
                orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(90)
            )
            form_layout.bind(minimum_height=form_layout.setter("height"))

            # Create a layout for checkboxes at the top
            checkbox_layout = GridLayout(
                cols=2,
                size_hint_y=None,
                spacing=dp(10),
                height=dp(40 * len(MAINTENANCE_OPTIONS)),
            )
            checkbox_layout.bind(minimum_height=checkbox_layout.setter("height"))

            # Create checkboxes, initially disabled
            checkboxes = []
            for option in MAINTENANCE_OPTIONS:
                checkbox_item = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )
                checkbox = MDCheckbox(
                    size_hint_x=None,
                    width=dp(40),
                    active=False,
                    disabled=True,
                    color_inactive=[26 / 255.0, 0, 0, 1],
                    color_active=[26 / 255, 0, 26 / 255, 1],
                )
                checkbox_item.add_widget(checkbox)
                checkboxes.append(checkbox)

                label = MDLabel(
                    text=option,
                    halign="left",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="Body",
                    role="large",
                    size_hint_x=0.6,
                )
                checkbox_item.add_widget(label)
                checkbox_layout.add_widget(checkbox_item)

            # Add checkbox layout at the top of the form
            form_layout.add_widget(checkbox_layout)

            # List of field names to generate labels and text inputs for
            fields = [
                "Object:",
                "Locataire:",
                "Cast Type:",
                "Serial Number:",
                "DOI:",
                "IMEI:",
                "Device ID:",
                "Client Name:",
                "Vehicle Type:",
                "IMMAT:",
                "Chassis:",
                "ICCID:",
                "Technician Name:",
            ]

            # Loop through each field to create MDLabel and TextInput pairs
            for field in fields:
                # Create a horizontal layout for label and input
                field_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )

                # Add the label
                field_label1 = MDLabel(
                    text=field,
                    size_hint_x=0.3,
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    halign="center",
                    font_style="Title",
                    role="large",
                )
                field_layout.add_widget(field_label1)

                if field == "Object:":
                    # Dropdown button
                    dropdown_button = MDButton(
                        MDButtonText(
                            text="Select Object",
                            theme_text_color="Custom",
                            text_color=(0, 0, 0, 1),
                        ),
                        size_hint=(0.4, None),
                        height=dp(40),
                        pos_hint={"x": 0, "center_y": 0.5},
                    )

                    # Create a new dropdown menu specific to this button and store it in the dictionary
                    menu_items = [
                        {
                            "text": obj,
                            "on_release": lambda x=obj, btn=dropdown_button, idx=i, checkboxes=checkboxes: self.set_object(
                                btn, x, idx, checkboxes
                            ),
                            "theme_text_color": "Custom",
                            "text_color": (198 / 255.0, 57 / 255.0, 57 / 255.0, 1),
                        }
                        for obj in OBJECTS
                    ]
                    dropdown_menu = MDDropdownMenu(
                        caller=dropdown_button, items=menu_items, width_mult=4
                    )

                    # Store the dropdown menu in the dictionary
                    self.dropdown_menus[i] = dropdown_menu
                    dropdown_button.bind(
                        on_release=lambda btn=dropdown_button, idx=i: self.dropdown_menus[
                            idx
                        ].open()
                    )
                    field_layout.add_widget(dropdown_button)

                else:
                    # Add the corresponding TextInput
                    field_input1 = TextInput(
                        hint_text=f"Enter {field[:-1].lower()}",
                        multiline=False,
                        size_hint_x=0.7,
                        height=dp(30),
                    )
                    field_layout.add_widget(field_input1)

                    # Add the horizontal field layout to the main form layout
                form_layout.add_widget(field_layout)

            # Add the form layout to the leasing_form
            leasing_screen.ids.leasing_form.add_widget(form_layout)
            self.forms.append(
                {"form": form_layout, "checkboxes": checkboxes}
            )  # Store the form and its checkboxes

        # Adjust the height of the parent MDBoxLayout to accommodate all children
        leasing_screen.ids.leasing_form.height = len(
            leasing_screen.ids.leasing_form.children
        ) * dp(40)

    def set_object(self, dropdown_button, selected_object, idx=None, checkboxes=None):
        """
        Set the object for the dropdown button.

        Args:
        - dropdown_button (MDButton): The dropdown button.
        - selected_object (str): The selected object.
        - idx (int, optional): The index of the form. Defaults to None.
        - checkboxes (list, optional): The list of checkboxes. Defaults to None.
        """
        if hasattr(dropdown_button, "children") and len(dropdown_button.children) > 0:
            for child in dropdown_button.children:
                if isinstance(child, MDButtonText):
                    child.text = selected_object
                    break

        print(f"Selected option: {selected_object}")  # Debugging info
        if idx is not None and idx < len(self.dropdown_menus):
            self.dropdown_menus[idx].dismiss()  # Dismiss the menu properly

        # Enable checkboxes if "MAINTENANCE" is selected
        if checkboxes is not None:
            if selected_object == "MAINTENANCE":
                for checkbox in checkboxes:
                    checkbox.disabled = False  # Enable checkboxes
            else:
                for checkbox in checkboxes:
                    checkbox.disabled = True  # Disable checkboxes
                    checkbox.active = False  # Uncheck if it was checked

    # Method to save the pdf for leasing vehicles
    def save_leasing_pdf(self):
        leasing_screen = self.root.get_screen("leasing")
        for form in leasing_screen.ids.leasing_form.children:
            pdf = CustomPDF("P", "mm", "A4")
            pdf.set_title("SMARTRACK ARCHIVE")
            pdf.set_author("GBETNKOM FARES")
            pdf.alias_nb_pages()
            pdf.add_page()

            # (Extract form data and build the PDF content as before)
            fields = [
                "Object",
                "Maintenance_opt",
                "Locataire",
                "Cast Type",
                "Serial Number",
                "DOI",
                "IMEI",
                "Device ID",
                "Client Name",
                "Vehicle Type",
                "IMMAT",
                "Chassis",
                "ICCID",
                "Technician Name",
            ]
            data: dict = {}
            maintenance_selections: list = []

            for field_layout in form.children:
                if (
                    isinstance(field_layout, MDBoxLayout)
                    and len(field_layout.children) > 1
                ):
                    label = field_layout.children[1]
                    input_field = field_layout.children[0]

                    if isinstance(input_field, TextInput):
                        field_name = label.text[:-1]
                        data[field_name] = input_field.text.upper()
                    elif isinstance(input_field, MDButton):
                        field_name = label.text[:-1]
                        data[field_name] = input_field.children[0].text
                elif isinstance(field_layout, GridLayout):
                    for checkbox_item in field_layout.children:
                        checkbox = checkbox_item.children[1]
                        label = checkbox_item.children[0].text
                        if checkbox.active:
                            maintenance_selections.append(label)

            data["Maintenance_opt"] = ", ".join(maintenance_selections)
            formatted_data = [{key: data.get(key, "") for key in fields}]
            pdf.table_vertical(formatted_data)

            # Get metadata for the archive entry
            client_name = data.get("Client Name", "Unknown_Client")
            locataire = data.get("Locataire", "Unknown_Locataire")
            immat = data.get("IMMAT", "Unknown_IMMAT")
            objet = data.get("Object", "")
            cast_type = data.get("Cast Type", "")
            serial_num = data.get("Serial Number", "")
            doi = data.get("DOI", "")
            imei = data.get("IMEI", "")
            device_id = data.get("Device ID", "")
            vehicle_type = data.get("Vehicle Type", "")
            chassis = data.get("Chassis", "")
            iccid = data.get("ICCID", "")
            technician_name = data.get("Technician Name", "")

            maintenance_opt = data.get("Maintenance_opt")

            # Instead of saving to a file, capture the PDF as binary data.
            # The output() method with dest="S" returns the PDF as a string, which we encode.
            pdf_data = bytes(pdf.output(dest="S"))

            # Insert the PDF and metadata into the database
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO archives (
                    pdf_type, client_name, locataire, immat,
                    object, cast_type, serial_number, doi, imei,
                    device_id, vehicle_type, chassis, iccid, technician_name,
                    maintenance_opt,  pdf_data
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    "leasing",
                    client_name,
                    locataire,
                    immat,
                    objet,
                    cast_type,
                    serial_num,
                    doi,
                    imei,
                    device_id,
                    vehicle_type,
                    chassis,
                    iccid,
                    technician_name,
                    maintenance_opt,
                    sqlite3.Binary(pdf_data),
                ),
            )
            self.conn.commit()
            print(
                f"PDF for leasing saved in database for client: {client_name}, immat: {immat}"
            )
            self.show_dialog(
                "Great!",
                f"Successfully saved leasing PDF in the database for {client_name}",
            )

    # Method used to create and manage the form for no_leasing vehicles
    def leasing_no(self, times):
        times = int(times)
        no_leasing_screen = self.root.get_screen("no_leasing")

        # Clear any existing widgets before adding new ones
        no_leasing_screen.ids.no_leasing_form.clear_widgets()

        # Store the different dropdown_menus
        self.dropdown_menus = {}
        self.forms = []  # Store the forms

        # Iterate for the number of times specified by the user
        for i in range(times):
            # Create a new vertical BoxLayout for the form
            form_layout = MDBoxLayout(
                orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(90)
            )
            form_layout.bind(
                minimum_height=form_layout.setter("height")
            )  # Dynamically set height

            # Create a layout for checkboxes at the top
            checkbox_layout = GridLayout(
                cols=2,
                size_hint_y=None,
                spacing=dp(10),
                height=dp(40 * len(MAINTENANCE_OPTIONS)),
            )
            checkbox_layout.bind(minimum_height=checkbox_layout.setter("height"))

            # Create checkboxes, initially disabled
            checkboxes = []
            for option in MAINTENANCE_OPTIONS:
                checkbox_item = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )
                checkbox = MDCheckbox(
                    size_hint_x=None, width=dp(40), active=False, disabled=True
                )  # Initially disabled
                checkbox_item.add_widget(checkbox)
                checkboxes.append(checkbox)  # Store reference for later use

                label = MDLabel(
                    text=option,
                    halign="center",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="Body",
                    role="large",
                    size_hint_x=0.6,
                )
                checkbox_item.add_widget(label)
                checkbox_layout.add_widget(checkbox_item)

            # Add checkbox layout at the top of the form
            form_layout.add_widget(checkbox_layout)

            # List of field names to generate labels and text inputs for
            fields = [
                "Object:",
                "Cast Type:",
                "Serial Number:",
                "DOI:",
                "IMEI:",
                "Device ID:",
                "Client Name:",
                "Vehicle Type:",
                "IMMAT:",
                "Chassis:",
                "ICCID:",
                "Technician Name:",
            ]

            # Loop through each field to create MDLabel and TextInput pairs
            for field in fields:
                # Create a horizontal layout for label and input
                field_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(40)
                )  # spacing=dp(10)

                # Add the label
                field_label2 = MDLabel(
                    text=field,
                    size_hint_x=0.3,
                    halign="center",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_style="Title",
                    role="large",
                )
                field_layout.add_widget(field_label2)

                if field == "Object:":
                    # Dropdown button
                    dropdown_button = MDButton(
                        MDButtonText(
                            text="Select Object",
                            theme_text_color="Custom",
                            text_color=(0, 0, 0, 1),
                        ),
                        size_hint=(0.4, None),
                        height=dp(40),
                        pos_hint={"x": 0, "center_y": 0.5},
                    )

                    # Create a new dropdown menu specific to this button and store it in the dictionary
                    menu_items = [
                        {
                            "text": obj,
                            "on_release": lambda x=obj, btn=dropdown_button, idx=i, checkboxes=checkboxes: self.set_object(
                                btn, x, idx, checkboxes
                            ),
                            "theme_text_color": "Custom",
                            "text_color": (198 / 255.0, 57 / 255.0, 57 / 255.0, 1),
                        }
                        for obj in OBJECTS
                    ]
                    dropdown_menu = MDDropdownMenu(
                        caller=dropdown_button, items=menu_items, width_mult=4
                    )

                    # Store the dropdown menu in the dictionary
                    self.dropdown_menus[i] = dropdown_menu
                    dropdown_button.bind(
                        on_release=lambda btn=dropdown_button, idx=i: self.dropdown_menus[
                            idx
                        ].open()
                    )
                    field_layout.add_widget(dropdown_button)
                else:
                    # Add the corresponding TextInput
                    field_input2 = TextInput(
                        hint_text=f"Enter {field[:-1].lower()}",  # Remove colon from field name for hint
                        multiline=False,
                        size_hint_x=0.7,
                        height=dp(30),
                    )
                    field_layout.add_widget(field_input2)

                # Add the horizontal field layout to the main form layout
                form_layout.add_widget(field_layout)

            # Add the form layout to the leasing_form
            no_leasing_screen.ids.no_leasing_form.add_widget(form_layout)
            self.forms.append(
                {"form": form_layout, "checkboxes": checkboxes}
            )  # Store the form and its checkboxes

        # Adjust the height of the parent MDBoxLayout to accommodate all children
        no_leasing_screen.ids.no_leasing_form.height = len(
            no_leasing_screen.ids.no_leasing_form.children
        ) * dp(40)

    # Method to save the pdf for no_leasing vehicles
    def save_no_leasing_pdf(self):
        no_leasing_screen = self.root.get_screen("no_leasing")

        for form in no_leasing_screen.ids.no_leasing_form.children:
            pdf = CustomPDF()
            pdf.set_title("SMARTRACK ARCHIVE")
            pdf.set_author("GBETNKOM FARES")
            pdf.alias_nb_pages()
            pdf.add_page()

            # Extract data from form fields
            fields = [
                "Object",
                "Maintenance_opt",
                "Cast Type",
                "Serial Number",
                "DOI",
                "IMEI",
                "Device ID",
                "Client Name",
                "Vehicle Type",
                "IMMAT",
                "Chassis",
                "ICCID",
                "Technician Name",
            ]
            data: dict = {}  # An empty dictionary that will store fields inputs
            maintenance_selections: list = (
                []
            )  # An empty list that will store the different maintenance_options

            for field_layout in form.children:
                if (
                    isinstance(field_layout, MDBoxLayout)
                    and len(field_layout.children) > 1
                ):
                    label = field_layout.children[1]
                    input_field = field_layout.children[0]

                    if isinstance(input_field, TextInput):
                        field_name = label.text[:-1]
                        data[field_name] = input_field.text.upper()
                    elif isinstance(input_field, MDButton):  # Check for dropdown button
                        field_name = label.text[:-1]
                        data[field_name] = input_field.children[
                            0
                        ].text  # Get the selected option
                elif isinstance(field_layout, GridLayout):  # Handle checkboxes
                    for checkbox_item in field_layout.children:
                        checkbox = checkbox_item.children[1]
                        label = checkbox_item.children[0].text
                        if checkbox.active:
                            maintenance_selections.append(label)

            # Include maintenance options
            data["Maintenance_opt"] = ", ".join(maintenance_selections)

            # Format data as a list of dictionaries for `table_vertical`
            formatted_data = [{key: data.get(key, "") for key in fields}]
            pdf.table_vertical(formatted_data)

            # Get metadata for the archive entry
            client_name = data.get("Client Name", "Unknown_Client")
            locataire = data.get("Locataire", "Unknown_Locataire")
            immat = data.get("IMMAT", "Unknown_IMMAT")
            objet = data.get("Object", "")
            cast_type = data.get("Cast Type", "")
            serial_num = data.get("Serial Number", "")
            doi = data.get("DOI", "")
            imei = data.get("IMEI", "")
            device_id = data.get("Device ID", "")
            vehicle_type = data.get("Vehicle Type", "")
            chassis = data.get("Chassis", "")
            iccid = data.get("ICCID", "")
            technician_name = data.get("Technician Name", "")

            maintenance_opt = data.get("Maintenance_opt")

            # Instead of saving to a file, capture the PDF as binary data.
            # The output() method with dest="S" returns the PDF as a string, which we encode.
            pdf_data = bytes(pdf.output(dest="S"))

            # Insert the PDF and metadata into the database
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO archives (
                    pdf_type, client_name, locataire, immat,
                    object, cast_type, serial_number, doi, imei,
                    device_id, vehicle_type, chassis, iccid, technician_name,
                    maintenance_opt, pdf_data
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    "no-leasing",
                    client_name,
                    None,
                    immat,
                    objet,
                    cast_type,
                    serial_num,
                    doi,
                    imei,
                    device_id,
                    vehicle_type,
                    chassis,
                    iccid,
                    technician_name,
                    maintenance_opt,
                    sqlite3.Binary(pdf_data),
                ),
            )
            self.conn.commit()
            print(
                f"PDF for no-leasing saved in database for client: {client_name}, immat: {immat}"
            )
            self.show_dialog(
                "Great!",
                f"Successfully saved no-leasing PDF in the database for {client_name}",
            )

    # Retrieve users from DB
    def retrieve_users_db(self) -> list:
        """Retrieves all usernames and passwords from the users table."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, user_name, password, role FROM users")
            users_data = cursor.fetchall()
            users: list = []
            # user_id: list = []
            for row in users_data:
                self.logged_in_user_ids = row[0]
                # user_id.append(self.logged_in_user_ids)
                # self.logged_in_user_id = user_id[0]
                users.append(
                    {
                        "id": row[0],
                        "user_name": row[1],
                        "password": row[2],
                        "role": row[3],
                    }
                )
            return users
        except sqlite3.Error as e:
            print(f"Database error retrieving users: {e}")
            self.show_dialog("Database Error", "Could not retrieve user list.")
            return []

    # Check the user's credentials before going to the MenuScreen
    def check_credentials(self, password, username):
        login_screen = self.root.get_screen("login")
        users = self.retrieve_users_db()  # Retrieve users from DB

        user_exists = False  # Flag to check if username exists
        password_exist = False

        for user in users:
            if username == user["user_name"]:
                user_exists = True  # Set flag to true as username is found
                if password == user["password"]:
                    password_exist = True
                    # Successful Login
                    user_role = user["role"]
                    if user_role == "admin":
                        self.nextScreen("menu")
                        # Clear fields and error label after successful login
                        login_screen.ids.username_field.text = ""
                        login_screen.ids.password_field.text = ""
                        login_screen.ids.error_label.text = ""
                        self.update_last_login(username)
                        return
                    elif user_role == "editor":
                        self.nextScreen("menu2")
                        # Clear fields and error label after successful login
                        login_screen.ids.username_field.text = ""
                        login_screen.ids.password_field.text = ""
                        login_screen.ids.error_label.text = ""
                        self.update_last_login(username)
                        return
                    elif user_role == "viewer":
                        self.nextScreen("menu3")
                        # Clear fields and error label after successful login
                        login_screen.ids.username_field.text = ""
                        login_screen.ids.password_field.text = ""
                        login_screen.ids.error_label.text = ""
                        self.update_last_login(username)
                        return
                else:
                    # Username exists, but password is incorrect
                    login_screen.ids.error_label.text = "Incorrect password"
                    return  # Exit, password incorrect

        if (not user_exists and not password_exist) or not user_exists:
            # Loop finished, username not found in users list
            login_screen.ids.error_label.text = "Account doesn't exist"

    # Update the last_login time of the user
    def update_last_login(self, username):
        """Updates the last_login timestamp for a user in the database."""
        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE users
                SET last_login = CURRENT_TIMESTAMP
                WHERE user_name = ?
            """
            cursor.execute(query, (username,))
            self.conn.commit()
            print(f"Last login updated for user: {username}")
        except sqlite3.Error as e:
            print(f"Database error updating last login time: {e}")

    # Method to check when scrolling has reached down
    def check_scroll_1(self, instance, value):
        leasing_screen = self.root.get_screen("leasing")
        if value <= 0:
            leasing_screen.ids.save_button.opacity = 1
            leasing_screen.ids.save_button.disabled = False
            # leasing_screen.ids.go_back.opacity = 1
            # leasing_screen.ids.go_back.disabled = False
        else:
            leasing_screen.ids.save_button.opacity = 0
            leasing_screen.ids.save_button.disabled = True
            # leasing_screen.ids.go_back.opacity = 0
            # leasing_screen.ids.go_back.disabled = True

    def check_scroll_2(self, instance, value):
        no_leasing_screen = self.root.get_screen("no_leasing")
        if value <= 0:
            no_leasing_screen.ids.save_button.opacity = 1
            no_leasing_screen.ids.save_button.disabled = False
            # no_leasing_screen.ids.go_back.opacity = 1
            # no_leasing_screen.ids.go_back.disabled = False
        else:
            no_leasing_screen.ids.save_button.opacity = 0
            no_leasing_screen.ids.save_button.disabled = True
            # no_leasing_screen.ids.go_back.opacity = 0
            # no_leasing_screen.ids.go_back.disabled = True

    def check_scroll_3(self, instance, value):
        no_leasing_screen = self.root.get_screen("edit_no_leasing")
        if value <= 0:
            no_leasing_screen.ids.update_button.opacity = 1
            no_leasing_screen.ids.update_button.disabled = False
            # no_leasing_screen.ids.go_back.opacity = 1
            # no_leasing_screen.ids.go_back.disabled = False
        else:
            no_leasing_screen.ids.update_button.opacity = 0
            no_leasing_screen.ids.update_button.disabled = True
            # no_leasing_screen.ids.go_back.opacity = 0
            # no_leasing_screen.ids.go_back.disabled = True

    def check_scroll_4(self, instance, value):
        no_leasing_screen = self.root.get_screen("edit_leasing")
        if value <= 0:
            no_leasing_screen.ids.update_button2.opacity = 1
            no_leasing_screen.ids.update_button2.disabled = False
            # no_leasing_screen.ids.go_back.opacity = 1
            # no_leasing_screen.ids.go_back.disabled = False
        else:
            no_leasing_screen.ids.update_button2.opacity = 0
            no_leasing_screen.ids.update_button2.disabled = True
            # no_leasing_screen.ids.go_back.opacity = 0
            # no_leasing_screen.ids.go_back.disabled = True

    def show_dialog(self, title: str, text: str):
        self.button = MDButton(
            MDButtonText(text="Ok"),
            on_release=lambda x: (self.dialog.dismiss(), self.previousScreen()),
        )
        if hasattr(self, "dialog") and self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text=title,
                halign="left",
                bold=True,
                font_style="Headline",
                role="large",
            ),
            MDDialogSupportingText(
                text=text, halign="left", bold=True, role="large", font_style="Body"
            ),
            MDDialogButtonContainer(Widget(), self.button),
            size_hint=(0.6, None),
            height=dp(200),
            scrim_color=(1, 1, 1, 1),
            radius=[dp(8), dp(8), dp(8), dp(8)],
        )
        self.dialog.open()

    @infos  # Apply the decorator correctly
    def close_app(self) -> None:
        MDApp.get_running_app().stop()
        Window.close()

    # Go to the previous screen
    def previousScreen(self) -> None:
        if self.screen_history:  # Checks if the self.screen_history list is not empty
            # removes the last previous screen visited
            previous_sreen = (
                self.screen_history.pop()
            )  # return previous visited screen to the variable
            print(f"Switching from {self.sm.current} to {previous_sreen} screen")
            self.sm.current = (
                previous_sreen  # Navigates directly back to the previous sreen
            )

    # Method used to store screens to the navigation history and go to the next screen
    def nextScreen(self, screen_name: str) -> None:
        # Push the current screen onto the stack
        current_screen = self.sm.current
        if (
            current_screen != screen_name
        ):  # Check the current screen before switching screens
            print(f"Switching from {current_screen} to {screen_name} screen")
            self.screen_history.append(
                current_screen
            )  # Adds the current screen to the navigation history
            self.sm.current = screen_name  # Then, switch to the next screen


if __name__ == "__main__":
    MyApp().run()
