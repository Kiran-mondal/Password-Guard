from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDSwitch
from password_utils import check_leak, password_strength

class PasswordGuardApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        screen = MDScreen()

        # Title
        title = MDLabel(
            text="🔐 Password Guard",
            halign="center",
            font_style="H4",
            pos_hint={"center_y": 0.9}
        )

        # Input field
        self.input = MDTextField(
            hint_text="Enter Password",
            password=True,
            helper_text="We never store your password.",
            helper_text_mode="on_focus",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            size_hint_x=0.85,
        )

        # Button
        check_btn = MDRaisedButton(
            text="CHECK",
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            on_release=self.check_button
        )

        # Theme switch
        self.switch = MDSwitch(pos_hint={"center_x": 0.9, "center_y": 0.95})
        self.switch.bind(active=self.change_theme)

        screen.add_widget(self.switch)
        screen.add_widget(title)
        screen.add_widget(self.input)
        screen.add_widget(check_btn)

        return screen

    def change_theme(self, *args):
        self.theme_cls.theme_style = "Dark" if self.switch.active else "Light"

    def check_button(self, *args):
        password = self.input.text
        if not password:
            self.show_popup("⚠️ Enter a password first!")
            return

        strength, entropy = password_strength(password)

        if check_leak(password):
            msg = f"⚠️ LEAKED PASSWORD!\nStrength: {strength}\nEntropy: {entropy} bits\n❌ Change immediately!"
        else:
            msg = f"✔️ Safe from leaks\nStrength: {strength}\nEntropy: {entropy} bits"

        self.show_popup(msg)

    def show_popup(self, message):
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Result",
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

PasswordGuardApp().run()
