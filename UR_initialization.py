from config import UR_IP_ADDRESS, DEFAULT_POSITION
import rtde_control
import rtde_receive

try:
    # Inicializace rozhraní pro kontrolu a příjem dat z robotického ramene Universal Robots
    rtde_c = rtde_control.RTDEControlInterface(UR_IP_ADDRESS) 
    rtde_r = rtde_receive.RTDEReceiveInterface(UR_IP_ADDRESS)

    # Kontrola, zda je připojení k oběma rozhraním úspěšné
    if rtde_c.isConnected() and rtde_r.isConnected():
        print("Úspěšně připojeno k robotickému rameni.")
        
        # Nastavení robota na výchozí pozici pomocí Inverse Kinematics
        rtde_c.moveJ_IK(DEFAULT_POSITION)
        # rtde_c.moveL(DEFAULT_POSITION)

    else:
        print("Připojení k robotickému rameni se nezdařilo.")
        
except Exception as e:
    print(f"Nastala chyba při komunikaci s robotem: {e}")