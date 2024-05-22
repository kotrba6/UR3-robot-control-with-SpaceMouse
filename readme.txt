README

Přehled
Tento projekt se skládá z modulárního programu určeného pro ovládání robotického ramene Universal Robots. Kód je strukturován do několika modulů, z nichž každý slouží specifickému účelu v celkovém systému. Níže je uveden přehled funkcí poskytovaných jednotlivými moduly.

Doporučení: Pro zajištění hladkého průběhu instalace a provozu doporučujeme tento kód spouštět na operačním systému Linux. Instalace knihovny ur_rtde je na Linuxových systémech výrazně jednodušší.

Moduly


1. USB_initialization.py
Tento modul je zodpovědný za inicializaci USB zařízení pomocí jeho Vendor ID a Product ID.

Závislosti: usb.core

Konfigurace:
Vendor ID a Product ID jsou definovány v souboru config.py.

Klíčové funkce:
Nalezení a inicializace USB zařízení.
Odpojení kernel driveru, pokud je aktivní.
Nastavení konfigurace a endpointu pro čtení dat.


2. config.py
Tento modul obsahuje různé konfigurační parametry použité v celém projektu.

Inicializace USB:
VENDOR_ID: Vendor ID USB zařízení.
PRODUCT_ID: Product ID USB zařízení.

Inicializace UR:
UR_IP_ADDRESS: IP adresa robotického ramene Universal Robots.
DEFAULT_POSITION: Výchozí pozice pro robotické rameno.

Ovládání UR:
Koeficienty a maximální rychlosti pro translaci a rotaci.
Velikost mrtvé zóny a délka paměti pro filtry.
EMA_COEF: Koeficient pro Exponenciální klouzavý průměr.
FIR_FILTER_COEFS: Koeficienty pro FIR filtr.


3. functions.py
Tento modul obsahuje různé pomocné funkce pro zpracování dat a ovládání.

Klíčové funkce:
bytes_to_int: Převod bajtů na celé číslo.
apply_fir_filter: Aplikace FIR filtru na vektor.
apply_ema_filter: Aplikace EMA filtru na hodnotu.
dead_zone_filter: Aplikace mrtvé zóny na vektor.
moving_average: Výpočet klouzavého průměru vektoru.
convert_to_speed_vector: Převod vektorů na rychlostní vektory pro translaci a rotaci.
collect_data_tool a collect_data_joint: Sběr dat o pozici nástroje a kloubů a jejich zápis do CSV souborů.


4. UR_control.py
Tento modul zajišťuje hlavní smyčku pro čtení dat z USB zařízení a ovládání robotického ramene podle potřeby.

Závislosti: usb.core, functions.py
Klíčové funkce:
Inicializace USB zařízení.
Zpracování dat z USB zařízení.
Aplikace různých filtrů na data.
Odesílání ovládacích příkazů robotickému rameni na základě zpracovaných dat.
Sběr dat o pozici nástroje a kloubů.


5. UR_initialization.py
Tento modul inicializuje připojení k robotickému rameni Universal Robots a nastaví jej do výchozí pozice.

Závislosti: rtde_control, rtde_receive

Klíčové funkce:
Inicializace kontrolního a přijímacího rozhraní pro robotické rameno.
Kontrola stavu připojení.
Přemístění robota do výchozí pozice pomocí inverzní kinematiky.


Instalace
Nainstalujte závislosti:
Ujistěte se, že máte nainstalovaný Python 3.x a pip. Poté nainstalujte závislosti pomocí následujícího příkazu:

bash
Zkopírovat kód
pip install -r requirements.txt

Nastavení: Ujistěte se, že máte správně nastaveny všechny konfigurační parametry v souboru config.py pro vaše prostředí.


Použití

Ovládání robota: Spusťte UR_control.py pro zahájení hlavní smyčky a ovládání robotického ramene.


Závislosti

Python 3.x
Knihovny: pyusb, ur_rtde
Poznámky
Ujistěte se, že IP adresa robota a ID USB zařízení jsou správně nastaveny v souboru config.py.
Kód obsahuje zpracování výjimek pro různé USB a komunikační chyby.
Smyčka v UR_control.py je navržena tak, aby běžela nepřetržitě, zpracovávala data a ovládala robota, dokud není přerušena.