
# Upute

## Pripremanje okruženja

Potrebno je instalirati python biblioteke koristeći sljedeću naredbu:
```console
pip install -r requirements.txt 
```

Potrebno je postaviti varijable okruženja koje sadrže važne informacije za rad projekta.

| Naziv | Opis |
| - | - |
| CLIENT_ID |  ID klijenta, koristi se za autentifikaciju s vanjskim API-jem. |
| CLIENT_SECRET |  Tajni ključ klijenta, koristi se za sigurnu komunikaciju s vanjskim API-jem. |
| LOGIN_URL |  URL za prijavu, koristi se za autentifikaciju korisnika. |
| BOT_TOKEN |  Token bota, koristi se za autentifikaciju i autorizaciju bota na platformi. |
| BOT_INVITE_LINK |  Poveznica za poziv bota, koristi se za pozivanje bota na različite servere ili kanale. |

## Pokretanje projekta

Projekt se pokreće sljedećom naredbom:
```console
python main.py
```
