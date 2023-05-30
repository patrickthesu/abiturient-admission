import db

connect = db.Connection ()

with open ('languages.csv') as file: 
    for language in file.read().strip().split("\n")[1:]:
        languageset = language.split(' ,')
        try:
            print (f"{languageset[3]} {languageset[4]}")
            connect.insertLanguage (languageset[3], languageset[4].replace('"', "").strip())
        except Exception as err:
            print (err)
