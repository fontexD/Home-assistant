Hey!

For at dette kan lade sig gøre skal man bruge denne usb-enhed 
https://www.aliexpress.com/item/1005001621816794.html
Samt 1 stk netværkskabel imellem inverter i RS485 port -> ens Home-assistant server/enhed/computer.


<b>Step 1.</b> indsæt USB-TTL i Ha-enheden (Pi4-nuc-bærebar) whatever man bruger til kører sin ha på, sæt netværkkabel i inverter i RS485 port, i den anden ende KLIP stik af og sæt følgende på USB-TTL enhed<br>
Hel blå B<br>
Hvid blå A<br>
<br>

![1](https://github.com/fontexD/Home-assistant/assets/87015443/023c5033-bb5f-4c67-a81b-3faa5fcad26c)

<br>

![2](https://github.com/fontexD/Home-assistant/assets/87015443/41a5f174-3006-4a66-84e7-593eb8974fa9)

<br>

![3](https://github.com/fontexD/Home-assistant/assets/87015443/6a68fabf-b7d3-4543-92f1-506bbad13bed)

<br>
Video guide til indstille inverter: https://www.dropbox.com/scl/fi/5pqa7w1votx2jxwkfy9v4/VID20230925164749.mp4?rlkey=z5qdqrt1hivjlr419w1vu3gcf&dl=0
<br>
<br>


Step 2. På inverter hold OK nede i 5-10 sekunder giv slip, pil op eller ned indtil RS485 kommer frem Tryk ok, ok igen og sæt den på VPP (for den kan snakke til ha over usb enheder)
VIGTIG INFO hvis du bruger rs485 til kommunikere med batteri så kan denne løsning ikke lade sig gøre, jeg bruger et alm growatt batteri, den bruger ikke den port, den brgues ofte hvis man bruger noget 3.part batteri, men det finder man ud af når man ser om porten er ledig.

Step 3. Indstillinger --> System --> Hardware --> Al hardware, Scroll ned indtil du kommer tili usb enheder de ser sådan her ud ttyUSB0 ttyUSB1 ttyUSB2 alt efter hvor mange usb devices der sidder i
den hedder ofte noget med "dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0" fold den ud og koper alt udfor ID: i mit filfælde "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"

<br>
<br>

Step 4. I Hacs Hent SolaX Inverter Modbus

<br>



Step 5. gå i Indstillinger --> Enheder og tjenster --> Tilføj Integration --> Solax Inveter MODBUS opsæt som følgende ->
<br>

Video guide til opsætning i HA : https://www.dropbox.com/scl/fi/q5qz8r6nc7o99iwtz3pgr/videoguide.mkv?rlkey=tthhx5nupirpwkfivrjznh8sg&dl=0

<br>
![1](https://github.com/fontexD/Home-assistant/assets/87015443/44abda9b-8038-45be-8dbe-e0548f0eecd0) 
<br>
![2](https://github.com/fontexD/Home-assistant/assets/87015443/d99f34d9-0224-4fb5-b013-97218e86dd03)
