# Integrering af Solcelle Inverter i Home Assistant

## Introduktion

Denne guide vil guide dig igennem processen med at integrere din solcelle inverter med Home Assistant ved hjælp af en USB-TTL-adapter og et RS485-netværkskabel.

For at gennemføre dette, vil du have brug for følgende:
- [USB-TTL Adapter](https://www.aliexpress.com/item/1005001621816794.html)
- Et RS485-netværkskabel til at forbinde inverteren til din Home Assistant-server eller enhed.

## Trin 1: Hardwareopsætning

1. Indsæt USB-TTL-adapteren i din Home Assistant-enhed (f.eks. Raspberry Pi, NUC, bærbar computer).
2. Tilslut RS485-netværkskablet til inverterens RS485-port.
3. I den anden ende af kablet skal du klippe stikket af og forbinde ledningerne som følger:
    - Blå ledning -> B
    - Hvid-blå ledning -> A

![1](https://github.com/fontexD/Home-assistant/assets/87015443/023c5033-bb5f-4c67-a81b-3faa5fcad26c)

<br>

![2](https://github.com/fontexD/Home-assistant/assets/87015443/41a5f174-3006-4a66-84e7-593eb8974fa9)

<br>

![3](https://github.com/fontexD/Home-assistant/assets/87015443/6a68fabf-b7d3-4543-92f1-506bbad13bed)

## Trin 2: Konfigurér Inverteren

1. Hold "OK"-knappen på inverteren nede i 5-10 sekunder og slip den.
2. Brug op eller ned knapperne indtil "RS485" vises på skærmen.
3. Tryk på "OK", og tryk derefter igen på "OK" for at vælge "VPP" (til kommunikation med Home Assistant via USB-enheder).

**Vigtigt:** Hvis du bruger RS485 til kommunikation med et batteri, kan denne løsning  ikke bruges. Denne vejledning antager brugen af et standard Growatt-batteri, der ikke bruger RS485-porten. Hvis du bruger et tredjepartsbatteri, skal du kontrollere, om porten er tilgængelig.

## Trin 3: Identificér USB-enheds-ID

1. I Home Assistant, gå til "Konfiguration" > "System" > "Hardware."
2. Rul ned til sektionen med USB-enheder; du vil se poster som "ttyUSB0," "ttyUSB1," "ttyUSB2," afhængig af antallet af tilsluttede USB-enheder.
3. Find posten, der ligner dette: "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0."
4. Kopier alt efter "ID:"; for eksempel "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0."

## Trin 4: Installer SolaX Inverter Modbus Integration

I Home Assistant, naviger til HACS (Home Assistant Community Store) og søg efter "SolaX Inverter Modbus." Installer integrationen.

## Trin 5: Opsæt Integration

1. Gå til "Konfiguration" > "Enheder og tjenester" > "Tilføj Integration."
2. Søg efter "SolaX Inverter MODBUS" og følg vejledningen på skærmen for at konfigurere integrationen.

For en detaljeret videoinstruktion om opsætning af denne integration i Home Assistant, se [denne video](https://www.dropbox.com/scl/fi/q5qz8r6nc7o99iwtz3pgr/videoguide.mkv?rlkey=tthhx5nupirpwkfivrjznh8sg&dl=0).

![1](https://github.com/fontexD/Home-assistant/assets/87015443/44abda9b-8038-45be-8dbe-e0548f0eecd0) 

![2](https://github.com/fontexD/Home-assistant/assets/87015443/d99f34d9-0224-4fb5-b013-97218e86dd03)


