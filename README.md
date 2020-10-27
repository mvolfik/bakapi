# Bakaláři API v3 client

```
Baka(láři)
   API
------
Bakapi
```

Jednoduchý klient k API Bakalářů pro Python.

## Changelog

### 0.3 (2020-10-27)
 - Nyní jsou defaultně používané timezone-aware datetimes. Pokud je `token_valid_until`
   timezone-unaware, předpokládá se že je v UTC.

 - Přidán volitelný parametr `to` k domácím úkolům, viz změny v [API dokumentaci](https://github.com/bakalari-api/bakalari-api-v3/blob/master/moduly/%C3%BAkoly.md)

### 0.2 (2020-10-13)
 - Umožnění vytvoření klienta bez hesla, pouze z `refresh_token`u, případně spolu s
   `access_token`em a jeho platností.

 - Přidán volitelný parametr `since` k domácím úkolům. Když není zadán, tak Bakaláři
   vrátí jen úkoly z posledních dvou měsíců (viz [API dokumentace](https://github.com/bakalari-api/bakalari-api-v3/blob/master/moduly/%C3%BAkoly.md))

### 0.1 (2020-04-09)
První release

## Dokumentace

_The code is the documentation. (Pls naučte mě někdo Sphinx)_

Modul obsahuje hlavní třídu `BakapiUser`.

Konstruktor vždy vyžaduje dva **keyword** argumenty: `url` a `username`. Dále vyžaduje
buď `password`, které je okamžitě použito k získání `access_token`u, nebo
`refresh_token`, volitelně spolu s `access_token` a `token_valid_until`. Ty jsou
uloženy a token je v případě potřeby obnoven až při prvním API požadavku.

### Metody instancí `BakapiUser`

`send_request(endpoint, method="GET", **kwargs)` zkontroluje platnost
`access_token`u, případně ho obnoví. Poté pošle požadavek s autorizačním headrem.
`kwargs` jsou předány metodě
[`requests.request`](https://requests.readthedocs.io/en/latest/api/#requests.request).  
Vrací [`requests.Response`](https://requests.readthedocs.io/en/latest/api/#requests.Response)

`query_api(endpoint, method="GET", **kwargs)` volá `send_request`, pouze navíc
ověřuje, že dostala validní JSON odpověď.  
Vrací naparsovaná data jako `dict`

`get_user_info()` získá informace o uživateli, vrací `dict` tak, jak ho dostane od
Bakalářů. Vypadá zhruba takto:

```python
{'UserUID': '...',
 'Class': <trida>,
 'FullName': '...',
 'SchoolOrganizationName': '...',
 'SchoolType': None,
 'UserType': 'student',
 'UserTypeText': 'žák',
 'StudyYear': 1,
 'EnabledModules': [
    {'Module': '<nazev modulu>', 'Rights': ['...']}
  ],
 'SettingModules': {'...?'}
}
```

Známé názvy modulů:  
Komens, Absence, Events, Marks, Timetable, Substitutions, Subjects, Homeworks, Gdpr

Třída je jednoduchý `dict`, vypadá takto:

```python
{'Id': '...', 'Abbrev': '...', 'Name': '...'}
```

`get_homework()` získá seznam všech úkolů, vrací `dict` tak, jak ho dostane od
Bakalářů. Přijímá volitelný parametr `since`, kterým lze omezit datum, od kterého jsou
brané úkoly. Může být `datetime.date`, `datetime.datetime` nebo `"YYYY-MM-DD"`.
Odpověď vypadá takto:

```python
{"Homeworks": [
    <ukoly>
  ]
}
```

Každý úkol vypadá zhruba takto:

```python
{'ID': '...',
 'DateAward': '0001-01-01T00:00:00+01:00',
 'DateControl': None,
 'DateDone': '0001-01-01T00:00:00+01:00',
 'DateStart': '0001-01-01T00:00:00+01:00',
 'DateEnd': '0001-01-01T00:00:00+01:00',
 'Content': '...',
 'Notice': '',
 'Done': True,
 'Closed': True,
 'Electronic': False,
 'Hour': 6,
 'Class': <trida>,
 'Group': <skupina>,
 'Subject': <predmet>,
 'Teacher': <ucitel>,
 'Attachments': [<prilohy>]}
```

Třída, skupina, předmět a učitel jsou jednoduchý `dict`, viz třída u `get_user_info()`

Každá příloha vypadá takto:

```python
{'Id': '...',
     'Name': '...',
     'Type': 'mime/type'}
```

`get_received_komens_messages()` získá seznam všech přijatých zpráv v Komens, vrací
`dict` tak, jak ho dostane od Bakalářů. Vypadá takto:

```python
{"Messages": [
    <zpravy>
  ]
}
```

Každá zpráva vypadá zhruba takto:

```python
{'$type': 'GeneralMessage',
 'Id': '...',
 'Title': 'Obecná zpráva',
 'Text': '...',
 'SentDate': '0001-01-01T00:00:00+01:00',
 'Sender': <odesilatel>,
 'Attachments': [<prilohy>],
 'Read': True,
 'LifeTime': 'ToRead',
 'DateFrom': None,
 'DateTo': None,
 'Confirmed': True,
 'CanConfirm': False,
 'Type': 'OBECNA',
 'CanAnswer': True,
 'Hidden': False,
 'CanHide': True,
 'RelevantName': '...',
 'RelevantPersonType': 'teacher|administrator|...?'}
```

Odesílatel je jednoduchý `dict`, viz třída u `get_user_info()`

Pro formát přílohy viz úkoly.

`download_attachment(attachment_id)` stáhne přílohu s daným ID.  
Vrací dvojici `filename`,
[`urllib3.response.HTTPResponse`](https://urllib3.readthedocs.io/en/latest/reference/index.html#urllib3.response.HTTPResponse)

**Dokumentace endpointů je průběžně vytvářena v repozitáři
[bakalari-api/bakalari-api-v3](https://github.com/bakalari-api/bakalari-api-v3)**

## Ukázky

### Použití přímo

```python console
>>> from bakapi import BakapiUser
>>> u = BakapiUser(url="https://bakalari.skola.cz", username="jan_novak", password="honzikovoHeslo")
>>> u.get_homework()
{'Homeworks': [
  {'ID': 'ABCDEFG',
   '...': '...',
   'Attachments': [
     {'Id': 'EFAAAAG',
      'Name': 'Ukol.doc',
      'Type': 'application/msword'}]
  },
  '...'
]}
>>> with open("Ukol.doc", "wb") as fh:
...   fh.write(u.download_attachment("EFAAAAG")[1].read())
```

### Použití jako Mixin

Knihovnu lze také použít jako Mixin do vaší vlastní classy uživatele.

Pokud například chcete ve své aplikaci ukládat data do databáze pomocí SQLAlchemy,
vytvořte classu uživatel takto:

```python
class User(BakapiUser, DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)

    # API používá tyto properties:
    url = Column(String)
    username = Column(String)
    token_valid_until = Column(DateTime)
    refresh_token = Column(String)
    access_token = Column(String)

    # další data, která používá vaše aplikace
    more_data = Column(String)

u = User(
    url="https://bakalari.skola.cz",
    username="jan_novak",
    password="honzikovoHeslo",
    more_data="neco"
)
```

- Je důležité, aby BakapiUser byl v seznamu inherited classes první, protože on předává
nepotřebné init parametry. Ostatní classy to ale dělat nemusí (a právě např.
DeclarativeBase to nedělá).
- Nemusíte definovat metodu `__init__`, ale pokud ji definujete, musí volat
`super().__init__()`
- Konstruktor příjímá povinné keyword argumenty (viz začátek). Cokoliv
dalšího pošle dál

Pro pochopení doporučuji
[tuto StackOverflow answer](https://stackoverflow.com/a/50465583/7292139)
