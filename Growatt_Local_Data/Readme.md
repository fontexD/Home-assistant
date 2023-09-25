Hey!

For at dette kan lade sig gøre skal man bruge denne usb-enhed 
https://www.aliexpress.com/item/1005001621816794.html
Samt 1 stk netværkskabel imellem inverter i RS485 port -> ens Home-assistant server/enhed/computer.


Step 1. indsæt USB-TTL i Ha-enheden (Pi4-nuc-bærebar) whatever man bruger til kører sin ha på, sæt netværkkabel i inverter i RS485 port, i den anden ende KLIP stik af og sæt følgende på USB-TTL enhed<br>
Hel blå B<br>
Hvid blå A<br>
<br>

![1](https://github.com/fontexD/Home-assistant/assets/87015443/b19289ad-2ff2-4d60-8b00-3f576bb9901f)
<br>
![2](https://github.com/fontexD/Home-assistant/assets/87015443/572d94d0-3c99-4c69-95d3-d511a4b863e2)

<br>

![3](https://github.com/fontexD/Home-assistant/assets/87015443/87737c65-77c6-4b65-bdae-ad82c4a1dcc1)

<br>

Step 2. Indstillinger --> System --> Hardware --> Al hardware, Scroll ned indtil du kommer tili usb enheder de ser sådan her ud ttyUSB0 ttyUSB1 ttyUSB2 alt efter hvor mange usb devices der sidder i
den hedder ofte noget med "dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0" fold den ud og koper alt udfor ID: i mit filfælde "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"

<br>
<br>

Step 3. I Hacs Hent SolaX Inverter Modbus

<br>

Step 4. gå i Indstillinger --> Enheder og tjenster --> Tilføj Integration --> Solax Inveter MODBUS opsæt som følgende ->
<br>
<br>
![1](https://github.com/fontexD/Home-assistant/assets/87015443/44abda9b-8038-45be-8dbe-e0548f0eecd0) 
<br>
![2](https://github.com/fontexD/Home-assistant/assets/87015443/d99f34d9-0224-4fb5-b013-97218e86dd03)
