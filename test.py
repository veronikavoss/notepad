from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QLocale


available_locales = QLocale().uiLanguages()
for locale in available_locales:
    country = QLocale(locale).countryToString(QLocale(locale).country())
    print(f"Country: {country}")