
class PasswordManager:

    def __init__(self, name=input("Enter the file name:\n")):
        self._diction_sites = {}
        self._name = name

    @property
    def diction_sites(self):
        return self._diction_sites

    def show_content(self):
        try:
            with open(self._name + ".txt", "r") as f:
                content = f.readlines()
                for row in content:
                    print(row)
        except FileNotFoundError:
            print("No such file")

    def _load_file(self, site, password):
        with open(self._name + ".txt", "a+") as f:
            f.write(f"{site}:{password}\n")

    def add_entry(self, site, password):
        if site in self._diction_sites.keys():
            print("Site is already inside")
        else:
            self.diction_sites[site] = password

    def delete_entry(self, site):
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
        with open(self._name + ".txt", "r") as f:
            content = f.readlines()
        for row in content:
            if site == row.split(":")[0]:
                password = row.split(":")[1].rstrip()
                statement = f"The password for {site} is {password}"
                return statement
        return "Your search was not found!"

    def save_all(self):
        for key, value in self._diction_sites.items():
            try:
                status = self._check_entry(key)
                if status:
                    self._load_file(key, value)
            except FileNotFoundError:
                self._load_file(key, value)
        self._diction_sites.clear()
        print("Your inputs were successfully written into the txt file")

    def _check_entry(self, key):
        cond = True
        with open(self._name + ".txt", "r") as f:
            content = f.readlines()
        for row in content:
            if key == row.split(":")[0]:
                cond = False
                break
        return cond

    def edit_entry(self, site):
        new_row = ""
        with open(self._name + ".txt", "r") as f:
            whole_text = f.read()
        if site in whole_text:
            with open(self._name + ".txt", "r") as f:
                content = f.readlines()
            for idx, rows in enumerate(content):
                if site == rows.split(":")[0]:
                    old_pass = rows.split(":")[1].rstrip()
                    new_pass = input("Enter the new password:\n")
                    new_row = rows.replace(old_pass, new_pass)
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
    else:
        print("Invalid command")
