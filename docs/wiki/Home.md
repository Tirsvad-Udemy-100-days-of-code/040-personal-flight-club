**English** · [Dansk](Home-da) · [Bahasa Malaysia](Home-ms)

# Personal Flight Club

A flight club from Day 40 of Udemy's 100 Days of Code. It reads destinations and price limits from a Google Sheet, finds the cheapest return flight for the next six months (direct first, then with stopovers) and emails every customer in a second sheet when a price is below the limit.

## How it works

1. Read the rows (city, IATA code, lowest price) from the `prices` sheet through Sheety.
2. Search the cheapest direct return flight from tomorrow to six months ahead for every row, with SerpAPI Google Flights or the course's mock flight service.
3. If there is no direct flight, search again for flights with up to two stops and note the number of stops.
4. If the price is lower than the sheet's lowest price, update the sheet, send a WhatsApp message and email every customer in the `users` sheet. A flight with stops says "Flight has 1 stopover." in the message.

## A sample run with mock data

![A sample run with mock data](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/raw/branch/main/docs/images/sample-run.png)

Next: [Getting started](Getting-Started)
