[English](Getting-Started) · **Dansk** · [Bahasa Malaysia](Getting-Started-ms)

# Kom i gang

## Krav

- Python 3.13 eller nyere
- Et Sheety-projekt til din kopi af Google Sheet med arkene `prices` og `users` (Bearer-godkendelse, PUT slået til på `prices`)
- En SerpAPI-nøgle eller adgangsoplysninger til mock-flyservicen
- En e-mailkonto med en app-adgangskode til at sende tilbudsmails
- Valgfrit: `pywhatkit`, en browser og en logget ind WhatsApp Web-session

## Opsætning

Opret et lokalt virtuelt miljø, opgradér pip og installér projektet:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Konfiguration

Kopiér `.env.example` til `.env` og udfyld værdierne. Læg aldrig `.env` i git. Hold dig til 3 til 5 destinationer i arket for at holde dig inden for de gratis grænser, og prøv programmet med et test-ark `users`, der kun indeholder din egen adresse.

| Variabel | Betydning |
| --- | --- |
| `SHEETY_PRICES_ENDPOINT` | Endpoint for arket `prices` |
| `SHEETY_USERS_ENDPOINT` | Endpoint for arket `users` (`firstName`, `lastName`, `email`) |
| `SHEETY_TOKEN` | Bearer-token til Sheety-projektet |
| `FLIGHT_PROVIDER` | `serpapi` eller `mock` |
| `SERPAPI_API_KEY` | SerpAPI-nøgle |
| `MOCK_FLIGHTS_APP_ID`, `MOCK_FLIGHTS_APP_KEY` | Adgangsoplysninger til mock-flyservicen |
| `SMTP_ADDRESS` | Din mailudbyders SMTP-server (port 587) |
| `EMAIL_ADDRESS`, `EMAIL_PASSWORD` | Afsenderadresse og dens app-adgangskode |
| `WHATSAPP_NUMBER` | Dit eget nummer med landekode |

## Kørsel

Start programmet. Uden SMTP-indstillinger eller WhatsApp-nummer bliver beskeden skrevet i konsollen i stedet.

```bash
python -m flight_club
```

## Test

Testene bruger intet netværk, sender ingen e-mails og læser aldrig din `.env`.

```bash
python -m pytest
```

![Testkørsel](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/raw/branch/main/docs/images/tests-run.png)
