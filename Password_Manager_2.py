from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self, name=input("Enter the file name:\n")):
        """Initialize new txt file which will contain all sites/passwords.
        Also it initialize a dictionary which will be used to safe all
        users input before saving them to the txt file.
        Creating key
        """
        self._diction_sites = {}
        self._name = name
        self._key = None

    @property
    def diction_sites(self):
        return self._diction_sites

    def create_key(self, name_key):
        """Creating encryption key"""
        self._key = Fernet.generate_key()
        with open(name_key, "wb") as f:
            f.write(self._key)

    def load_key(self, name_key):
        """Loading the encryption key"""
        try:
            with open(name_key, "rb") as f:
                self._key = f.read()
        except FileNotFoundError:
            print("No valid key file!")

    def show_content(self):
        """Showing the content of the created txt file."""
        try:
            with open(self._name + ".txt", "r") as f:
                content = f.readlines()
                for row in content:
                    print(row)
        except FileNotFoundError:
            print("No such file")

    def _load_file(self, site, password):
        """Used to load the content of the txt file."""
        try:
            with open(self._name + ".txt", "a+") as f:
                enc_pass = Fernet(self._key).encrypt(password.encode())
                f.write(f"{site}:{enc_pass.decode()}\n")
        except TypeError:
            print("You did not provide encrypting key!")

    def add_entry(self, site, password):
        """Adding site/password to the current dictionary."""
        if site in self._diction_sites.keys():
            print("Site is already inside")
        else:
            self.diction_sites[site] = password

    def delete_entry(self, site):
        """Deleting the entered site along with its password."""
        with open(self._name + ".txt", "r") as f:
            content = f.readlines()
        for idx, row in enumerate(content):
            site_inside = row.split(":")[0]
            if site == site_inside:
                content.pop(idx)
                print("The site with the password were successfully removed!")
                break
        with open(self._name + ".txt", "w") as f:
            for row in content:
                f.write(row)

    def search_entry(self, site):
        """Searching the site and showing it's password after being decrypted."""
        with open(self._name + ".txt", "r") as f:
            content = f.readlines()
            for row in content:
                site_input, password = row.split(":")
                if site == site_input:
                    decrypted_pass = Fernet(self._key).decrypt(password.encode()).decode()
                    statement = f"The password for {site} is {decrypted_pass}"
                    return statement
        return "Your search was not found!"

    def save_all(self):
        """Saving all inputs from the dictionary to the txt file
        and after that clearing the current dictionary.
        """
        if self._key:
            for key, value in self._diction_sites.items():
                try:
                    status = self._check_entry(key)
                    if status:
                        self._load_file(key, value)
                except FileNotFoundError:
                    self._load_file(key, value)
            self._diction_sites.clear()
            print("Your inputs were successfully written into the txt file")
        else:
            print("No encryption key is provided")

    def _check_entry(self, key):
        """Checking if some of the inputs in the dictionary
        are inside the txt file. If so - they won't be saved.
        """
        cond = True
        with open(self._name + ".txt", "r") as f:
            content = f.readlines()
        for row in content:
            if key == row.split(":")[0]:
                cond = False
                break
        return cond

    def edit_entry(self, site):
        """Check if the site is inside the txt file
        and if it is, it prompts for a new password.
        """
        new_row = ""
        with open(self._name + ".txt", "r") as f:
            whole_text = f.read()
        if site in whole_text:
            with open(self._name + ".txt", "r") as f:
                content = f.readlines()
            for idx, rows in enumerate(content):
                if site == rows.split(":")[0]:
                    new_pass = input("Enter the new password:\n")
                    value = Fernet(self._key).encrypt(new_pass.encode())
                    enc_new_pass = value.decode()
                    new_row = f"{site}:{enc_new_pass}"
                    content.pop(idx)
            with open(self._name + ".txt", "w") as f:
                f.write(new_row)
            with open(self._name + ".txt", "a+") as f:
                for row in content:
                    f.write(row)
            print(f"The update of {site} was successful")
        else:
            print("Your search was not found!")


pm = PasswordManager()
while True:

    print("""
    Choose from options below:\n
    (1) Show content
    (2) Add entry to current dictionary
    (3) Delete entry
    (4) Search entry
    (5) Quit
    (6) Show current entries in dictionary
    (7) Save to file
    (8) Edit site password
    (9) Create first encryption key
    (10) Load the decryption key
    """)

    user_command = input("Enter option: ")

    if user_command == "1":
        pm.show_content()
    elif user_command == "2":
        pm.add_entry(site=input("Enter site:"), password=input("Enter pass:"))
    elif user_command == "3":
        pm.delete_entry(site=input("Enter site:"))
    elif user_command == "4":
        print(pm.search_entry(site=input("Enter site:")))
    elif user_command == "5":
        print("Bye Bye!")
        break
    elif user_command == "6":
        print(pm.diction_sites)
    elif user_command == "7":
        pm.save_all()
    elif user_command == "8":
        pm.edit_entry(site=input("Enter site:"))
    elif user_command == "9":
        pm.create_key(name_key=(input("Name of the file to create: ") + ".key"))
    elif user_command == "10":
        pm.load_key(name_key=(input("Name of the file to load: ") + ".key"))
    else:
        print("Invalid command")
