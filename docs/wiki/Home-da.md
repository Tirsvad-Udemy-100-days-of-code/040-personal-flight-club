[English](Home) · **Dansk** · [Bahasa Malaysia](Home-ms)

# Personal Flight Club

En flyklub fra dag 40 i Udemys 100 Days of Code. Programmet læser destinationer og prisgrænser fra et Google Sheet, finder den billigste returflyvning de næste seks måneder (først direkte, derefter med mellemlandinger) og sender en e-mail til alle kunder i et andet ark, når en pris er under grænsen.

## Sådan virker det

1. Læs rækkerne (by, IATA-kode, laveste pris) fra arket `prices` via Sheety.
2. Søg efter den billigste direkte returflyvning fra i morgen til seks måneder frem for hver række, med SerpAPI Google Flights eller kursets mock-flyservice.
3. Hvis der ikke er en direkte flyvning, søges der igen efter flyvninger med op til to stop, og antallet af stop noteres.
4. Hvis prisen er lavere end arkets laveste pris, opdateres arket, der sendes en WhatsApp-besked, og alle kunder i arket `users` får en e-mail. En flyvning med stop siger "Flight has 1 stopover." i beskeden.

## Et eksempel på en kørsel med mock-data

![Et eksempel på en kørsel med mock-data](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/raw/branch/main/docs/images/sample-run.png)

Næste: [Kom i gang](Getting-Started-da)
