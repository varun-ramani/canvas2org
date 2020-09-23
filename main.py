from time import sleep

from selenium.webdriver.common.keys import Keys

from browserwrapper import BrowserWrapper

page_url = input("Enter URL of assignments page on ELMS > ")

browser = BrowserWrapper("Safari")

browser.load_page(page_url)

if browser.was_redirected():
    login_fields = browser.get_login_fields()

    if login_fields != None:
        print("Detected login page.")

        login_successful = False
        while not login_successful:

            username_element = login_fields['username']['element']
            username_label = login_fields['username']['label']
            password_element = login_fields['password']['element']
            password_label = login_fields['password']['label']

            username_element.clear()
            password_element.clear()

            username = input(f'Enter {username_label} > ')
            password = input(f'Enter {password_label} > ')

            username_element.send_keys(username)
            password_element.send_keys(password)
            password_element.send_keys(Keys.ENTER)

            sleep(2.5)

            login_fields = browser.get_login_fields()
            if login_fields != None:
                print("Login failed, please try again")

            else:
                login_successful = True

        browser.update_intended_page()
        print("Waiting for 2FA")
        browser.wait_for_next_page()
        print("2FA complete, redirecting to assignments page now")
        browser.update_intended_page()

    else:
        print("Detected unknown redirection - quitting now.")
        exit(-1)

browser.load_page(page_url)
print("Waiting 5 seconds for page to fully load...")
sleep(5)
browser.execute_js("document.querySelector(\"label[for='show_by_type']\").click()")

print('Switching to "Show by Type"')

org_lines = []

type_lists = browser.get_type_lists()

for type_list in type_lists:
    processed_list = browser.process_type_list(type_list)
    org_lines.append(f"* {processed_list['title']}")

    for assignment in processed_list['assignments']:
        org_lines.append(f"** TODO {assignment['title']}")
        org_lines.append(f"   DEADLINE: {assignment['deadline']}")

    org_lines.append("\n")

print("\n".join(org_lines))
