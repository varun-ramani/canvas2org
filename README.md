# Canvas 2 Org

Scrapes an assignments page on ELMS Canvas and converts it to an org-mode file, complete with deadlines and categorization. This
was my first time using Selenium, so this project is far from elegant. Consider it a hacky solution that somewhat works.

Note that ELMS Canvas does have an API, but accessing this requires an authtoken that the university needs to provide.

Run `python3 main.py`, follow the prompts, and the program will eventually output an org-mode file.
