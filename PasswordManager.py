import sqlite3

name_of_pm = ""


def connect():
    global name_of_pm
    name_of_pm = input("Enter the name of the new Password Manager:\n")
    conn = sqlite3.connect(name_of_pm + ".db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sites (site_title TEXT, password TEXT)")
    conn.commit()
    conn.close()


def add_entry():
    global name_of_pm
    site = input("\nEnter the site:\n").title()
    conn = sqlite3.connect(name_of_pm + ".db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sites WHERE site_title=?", (site,))
    if cur.fetchone()[0] == 1:
        print("This site is already entered!\n")
        conn.close()
    else:
        password = input("Enter the password for the site:\n")
        cur.execute("INSERT INTO sites VALUES (?, ?)", (site, password))
        conn.commit()
        conn.close()
        print("Your input was entered!\n")


def show_all():
    global name_of_pm
    conn = sqlite3.connect(name_of_pm + ".db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM sites")
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        print(f"{row[0]} -> {row[1]}")
    print()


def remove_entry():
    global name_of_pm
    site = input("Enter the site you want to delete:\n").title()
    conn = sqlite3.connect(name_of_pm + ".db")
    cur = conn.cursor()
    if not cur.execute("SELECT site_title FROM sites WHERE site_title=?", (site,)):
        print("The site does not exists!\n")
        conn.close()
    else:
        cur.execute("DELETE FROM sites WHERE site_title=?", (site,))
        conn.commit()
        conn.close()
        print("Delete was successful\n")


def search_entry():
    global name_of_pm
    site = input("Enter the site you want to search:\n").title()
    conn = sqlite3.connect(name_of_pm + ".db")
    cur = conn.cursor()
    if not cur.execute("SELECT site_title FROM sites WHERE site_title=?", (site,)):
        print("The site does not exists!\n")
        conn.close()
    else:
        cur.execute("SELECT * FROM sites WHERE site_title=?", (site,))
        row = cur.fetchall()
        conn.close()
        # print(row)
        print(f"The password for {site} is -> {row[0][1]}\n")


def edit_entry():
    global name_of_pm
    site = input("Enter the site you want to edit:\n").title()
    conn = sqlite3.connect(name_of_pm + ".db")
    cur = conn.cursor()
    if not cur.execute("SELECT site_title FROM sites WHERE site_title=?", (site,)):
        print("The site does not exists!\n")
        conn.close()
    else:
        new_password = input("Enter the new password:\n")
        cur.execute("UPDATE sites SET password=? WHERE site_title=?", (new_password, site))
        conn.commit()
        conn.close()
        print("The update was successful\n")


def main():

    connect()

    while True:

        print("""What do you want to do?
            (1) Add a site
            (2) Remove a site
            (3) Search a site
            (4) Edit a site
            (5) Show all inputs
            (6) Quit
            """)

        user_command = input("-->\t")

        if user_command == "1":
            add_entry()
        elif user_command == "2":
            remove_entry()
        elif user_command == "3":
            search_entry()
        elif user_command == "4":
            edit_entry()
        elif user_command == "5":
            show_all()
        elif user_command == "6":
            print("Bye Bye")
            break
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()
