import usb.core
from config import TRASLATION_COEF, ROTATION_COEF, TRANSLATION_MAX_SPEED, ROTATION_MAX_SPEED, DEAD_ZONE_SIZE, MEMOTY_LENGTH
from USB_initialization import device, endpoint
from functions import read_and_process_data, dead_zone_filter, moving_average, convert_to_speed_vector, collect_data_tool, collect_data_joint
from UR_initialization import rtde_c

# Čtení, zpracování a zápis dat
try:
    while True:
        try:
            # Čtení dat
            vector = read_and_process_data(device, endpoint)
            
            # Zavedení pásmové zádrže kolem 0
            dead_zone_vector = dead_zone_filter(vector, DEAD_ZONE_SIZE)

            # Přidání vektoru do klouzavého průměru a získání průměru
            MA_vector = moving_average(dead_zone_vector, MEMOTY_LENGTH)

            # Převedení do požadovaného formátu
            speed_vector = convert_to_speed_vector(MA_vector, TRASLATION_COEF, ROTATION_COEF, TRANSLATION_MAX_SPEED, ROTATION_MAX_SPEED)
            print(speed_vector)

            # Ovládání robota pomocí funkce jogStart
            rtde_c.jogStart(speed_vector, rtde_c.FEATURE_BASE, 0.5)

            # Sběr dat o pozici nástroje a kloubů robota a ápis sběraných dat do CSV souborů
            collect_data_tool("Tool_position.csv")
            collect_data_joint("Joint_position.csv")

        except usb.core.USBError as e:
            if "Operation timed out" in str(e):
                continue  # Pokračovat ve smyčce, pokud dojde k vypršení časového limitu
            else:
                print(f"USB error: {e}")
                break  # Přerušení smyčky v případě jiné USB chyby
except KeyboardInterrupt:
    print("\nProgram přerušen uživatelem.")
