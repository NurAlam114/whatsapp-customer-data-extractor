from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re


results = []


# patterns
phone_pattern = re.compile(
    r"^\+?\d[\d\s-]{8,}$"
)

date_pattern = re.compile(
    r"^(?:\d{1,2}/\d{1,2}/\d{4})$"
)

time_pattern = re.compile(
    r"^(?:\d{1,2}:\d{2}\s?(?:AM|PM))$",
    re.I
)


bad_words = [
    "Archived",
    "unread message",
    "messages",
    "You reacted",
    "You deleted",
    "This business is now using",
    "Messages and calls are now end-to-end encrypted",
    "added",
    "set the username",
]


def clean_text(x):
    return x.strip()


def is_bad(x):
    x = x.lower()

    for b in bad_words:
        if b.lower() in x:
            return True

    return False



with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="whatsapp_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://web.whatsapp.com"
    )

    print("Loading WhatsApp...")
    time.sleep(15)


    chat_box = page.locator(
        "div.x1n2onr6.x1vjfegm.x78zum5.xdt5ytf.x1iyjqo2.x1odjw0f.x1280gxy"
    )


    chat_box.evaluate(
        "(e)=>e.scrollTop=0"
    )

    time.sleep(3)


    collected = set()


    # SAME SCROLLING LOGIC
    for i in range(80):

        items = chat_box.locator(
            "div.x78zum5"
        )

        count = items.count()


        for j in range(count):

            try:

                text = items.nth(j).inner_text()


                lines = [
                    clean_text(x)
                    for x in text.split("\n")
                    if clean_text(x)
                ]


                if len(lines) < 2:
                    continue


                lines = [
                    x for x in lines
                    if not is_bad(x)
                ]


                if len(lines) < 2:
                    continue


                name = lines[0]
                last = lines[-1]


                if (
                    date_pattern.match(name)
                    or time_pattern.match(name)
                ):
                    continue


                if (
                    "group" in name.lower()
                    or "community" in name.lower()
                ):
                    continue


                phone = ""


                if phone_pattern.match(name):

                    phone = name
                    name = ""


                collected.add(
                    (
                        name,
                        phone,
                        last
                    )
                )


            except:
                pass



        chat_box.evaluate(
            "(e)=>e.scrollTop += 600"
        )

        time.sleep(1)


        print(
            "Scroll:",
            i,
            "Collected:",
            len(collected)
        )



    # SAVE EXCEL

    for name, phone, last in collected:


        timestamp = ""


        if date_pattern.match(last):

            timestamp = last


        elif time_pattern.match(last):

            timestamp = last



        # WhatsApp Link

        whatsapp_link = ""


        if phone:

            clean_number = re.sub(
                r"\D",
                "",
                phone
            )


            if clean_number.startswith("0"):

                clean_number = "88" + clean_number


            whatsapp_link = (
                "https://wa.me/" + clean_number
            )



        results.append({

            "Name": name,

            "Phone Number": phone,

            "Timestamp": timestamp,

            "WhatsApp Link": whatsapp_link

        })



    df = pd.DataFrame(results)


    df.drop_duplicates(
        inplace=True
    )


    df.to_excel(
        "clean_whatsapp_data.xlsx",
        index=False
    )


    print("====================")
    print(
        "FINAL ROWS:",
        len(df)
    )
    print(
        "Excel Created"
    )
    print("====================")


    browser.close()