# Ovládání robotu UR pomocí SpaceMouse
Czech/[English](README.md)
## Obsah
- [Úvod](#úvod)
- [Instalace](#instalace)
- [Použití](#použití)
- [Funkce](#funkce)
- [Konfigurace](#konfigurace)
- [Přispívání](#přispívání)

## Úvod
Tento projekt se skládá z modulárního programu určeného k inicializaci a ovládání USB zařízení a robotického ramene Universal Robot (UR). Program čte data z USB zařízení a zpracovává je pro ovládání pohybů robotického ramene.

## Instalace
### Požadavky
- Doporučeno spouštět na Linuxu pro snadnou instalaci knihovny `ur_rtde`.
- Python 3.x
- Potřebné Python knihovny:
  - `usb`
  - `ur_rtde`

### Kroky
1. Naklonujte repozitář:
    ```bash
    git clone https://github.com/kotrba6/UR3-robot-control-with-SpaceMouse.git
    cd UR3-robot-control-with-SpaceMouse
    ```
2. Nainstalujte závislosti:
    ```bash
    pip3 install -r requirements.txt
    ```

## Použití
### Spuštění programu
1. Nastavte parametry v souboru `config.py`:
   - Zadejte správné Vendor ID a Product ID USB zařízení.
   - Zadejte správnou IP adresu robotického ramene UR.
   - Nastavte maximální rychlost pro translaci a rotaci.
   - Nastavte výchozí polohu robotického ramene UR.

2. Spusťte skript `UR_control.py`:
    ```bash
    python UR_control.py
    ```

Po spuštění skriptu by mělo být možné ovládat robotické rameno pomocí SpaceMouse.

### Popis skriptů
- **USB_initialization.py**: Inicializuje USB zařízení pomocí Vendor ID a Product ID, nastaví konfiguraci zařízení a připraví endpoint pro čtení dat.
- **UR_initialization.py**: Naváže spojení s robotickým ramenem UR a přesune rameno do výchozí polohy.
- **UR_control.py**: Čte data z USB zařízení, zpracovává je a odpovídajícím způsobem ovládá pohyby robotického ramene UR.
- **functions.py**: Obsahuje pomocné funkce pro konverzi a zpracování dat.
- **config.py**: Definuje konfigurační parametry pro USB zařízení a robotické rameno UR.

## Funkce
- Inicializace a čtení dat z USB zařízení.
- Inicializace a ovládání robotického ramene UR.
- Funkce pro zpracování dat pro konverzi a filtrování dat.
- Konfigurační soubor pro snadné úpravy parametrů.

## Konfigurace
Soubor `config.py` obsahuje následující konfigurovatelné parametry:
- **USB_initialization**:
  - `VENDOR_ID`: Vendor ID USB zařízení.
  - `PRODUCT_ID`: Product ID USB zařízení.
- **UR_initialization**:
  - `UR_IP_ADDRESS`: IP adresa robotického ramene UR.
  - `DEFAULT_POSITION`: Výchozí poloha robotického ramene UR.
- **UR_control**:
  - `TRASLATION_COEF`: Koeficient pro výpočet rychlostních vektorů pro translaci.
  - `ROTATION_COEF`: Koeficient pro výpočet rychlostních vektorů pro rotaci.
  - `TRANSLATION_MAX_SPEED`: Maximální rychlost pro translaci [m/s].
  - `ROTATION_MAX_SPEED`: Maximální rychlost pro rotaci [rad/s].
  - `DEAD_ZONE_SIZE`: Velikost pásmové zádrže.
  - `MEMORY_LENGTH`: Délka paměti pro klouzavý průměr.

## Přispívání
Příspěvky jsou vítány! Prosím, následujte tyto kroky:
1. Vytvořte fork repozitáře.
2. Vytvořte novou větev (`git checkout -b feature-branch`).
3. Commitujte své změny (`git commit -m 'Přidání nové funkce'`).
4. Pushujte do větve (`git push origin feature-branch`).
5. Otevřete pull request.
