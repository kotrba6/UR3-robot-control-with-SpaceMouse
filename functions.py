from math import pi
import csv
from config import DEAD_ZONE_SIZE
from UR_initialization import rtde_r

def bytes_to_int(bytes):
    """
    Převádí dva bajty na jedno celé číslo se znaménkem.
    
    Args:
        bytes (list of int): Seznam dvou bajtů (0-255) k převodu.
    
    Returns:
        int: Převedená hodnota z bajtů na celé číslo.
    """

    value = bytes[0] + (bytes[1] << 8)
    if value > 32767:
        value -= 65536
    return value


def convert_to_int_vector(data):
    """
    Převádí seznam bajtů na vektor celých čísel reprezentující souřadnice.
    
    Args:
        data (list of int): Seznam bajtů obsahující souřadnice x, y, z.
    
    Returns:
        list of int: Vektor celých čísel [x, y, z].
    """

    coordinate_y = -bytes_to_int(data[1:3])
    coordinate_x = -bytes_to_int(data[3:5])
    coordinate_z = -bytes_to_int(data[5:7])

    int_vector = [coordinate_x, coordinate_y, coordinate_z]
    return int_vector


def read_vector(device, endpoint):
    """
    Čte data z zařízení a konvertuje je na vektor pomocí USB.
    
    Args:
        device: USB zařízení.
        endpoint: Koncový bod USB zařízení.
    
    Returns:
        list of int: Vektor celých čísel [x, y, z].
    """

    data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
    return convert_to_int_vector(data)


def read_and_process_data(device, endpoint):
    """
    Získává translaci a rotaci jako vektory a spojuje je do jednoho.
    
    Args:
        device: USB zařízení.
        endpoint: Koncový bod USB zařízení.
    
    Returns:
        list of int: Kombinovaný vektor translace a rotace.
    """

    translation_vector = read_vector(device, endpoint)
    rotation_vector = read_vector(device, endpoint)
    return translation_vector + rotation_vector


def shift_vector_values(vector, shift_value = DEAD_ZONE_SIZE):
    """
    Posune všechny hodnoty v šestimístném poli `vector` o hodnotu `shift_value`.
    Pokud je hodnota v poli větší než 0, odečte od n9 `shift_value`.
    Pokud je hodnota v poli menší než 0, přičte k n9 `shift_value`.

    Args:
    vector (list): Seznam obsahující hodnoty.
    shift_value: Hodnota, o kterou se mají prvky posunout.

    Returns:
    list: Seznam s upravenými hodnotami.
    """
    shifted_vector = []
    for value in vector:
        if value > 0:
            shifted_vector.append(value - shift_value)
        elif value < 0:
            shifted_vector.append(value + shift_value)
        else:
            shifted_vector.append(value)

    return shifted_vector


def dead_zone_filter(vector, dead_zone_size):
    """
    Aplikuje filtr mrtvé zóny na vektor pro eliminaci malých hodnot.
    
    Args:
        vector (list of int): Vstupní vektor.
        dead_zone_size (int): Velikost mrtvé zóny kolem 0 (10 -> fitrují se hodnoty od -10 do 10)
    
    Returns:
        list of int: Vektor s aplikovaným filtrem.
    """

    for index, value in enumerate(vector):
        if -dead_zone_size < value < dead_zone_size:
            vector[index] = 0

    shifted_vector = shift_vector_values(vector)

    return shifted_vector


def moving_average(new_vector, memory_length):
    """
    Vypočítá klouzavý průměr pro vstupní vektor na základě historie hodnot.
    
    Funkce udržuje historii posledních hodnot pro každou složku vektoru a vypočítá průměr
    z těchto hodnot, aby vyhladila krátkodobé fluktuace a odhalila dlouhodobé trendy.
    
    Args:
        new_vector (list of float): Nový vektor hodnot, pro který se má vypočítat průměr.
        memory_length (int): Délka paměti (počet prvků v historii pro každou složku vektoru).
    
    Returns:
        list of float: Vektor průměrných hodnot pro každou složku vstupního vektoru.
    
    Raises:
        ValueError: Pokud nový vektor nemá očekávaný počet složek, vyvolá výjimku.
    """
    
    # Inicializace historie, pokud ještě nebyla nastavena
    if not hasattr(moving_average, "history"):
        moving_average.history = [[] for _ in range(len(new_vector))]
        moving_average.vector_size = len(new_vector)

    # Kontrola konzistence velikosti vstupního vektoru
    if len(new_vector) != moving_average.vector_size:
        raise ValueError("Vektor nemá správnou velikost.")

    # Zkontrolovat, zda vektor obsahuje samé nuly
    if all(value == 0 for value in new_vector):
        # Přidat vektor do historie, ale vrátit původní vektor
        for i in range(moving_average.vector_size):
            moving_average.history[i].append(new_vector[i])
            # Upravuje délku historie na zadanou paměťovou délku.
            if len(moving_average.history[i]) > memory_length:
                moving_average.history[i].pop(0) # Odstranění nejstarší hodnoty
        return new_vector

    average = []    # Seznam pro ukládání vypočítaných průměrných hodnot
    for i in range(moving_average.vector_size):
        # Přidání nové hodnoty do odpovídající historie
        moving_average.history[i].append(new_vector[i])
        
        # Upravuje délku historie na zadanou paměťovou délku.
        # Pokud délka historie přesáhne zadanou paměťovou délku, odstraní nejstarší záznam.
        if len(moving_average.history[i]) > memory_length:
            moving_average.history[i].pop(0) # Odstranění nejstarší hodnoty
        
        # Výpočet průměru pro aktuální složku
        average.append(sum(moving_average.history[i]) / len(moving_average.history[i]))
    
    return average



def EMA_filter(current_ema, new_vector, alpha):
    """
    Aplikuje exponenciální klouzavý průměr (EMA) na pohybový vektor.

    Args:
        current_ema (list of float): Aktuální EMA vektor.
        new_vector (list of float): Nový pohybový vektor pro aplikaci EMA.
        alpha (float): Exponenciální faktor pro vážení nových a starých hodnot (0 < alpha < 1).

    Returns:
        list of float: Nový EMA pro každou složku vektoru.

    """

    if not current_ema:
        # Pokud je to první průchod a EMA není inicializováno, použijeme nový vektor jako počáteční EMA.
        return new_vector
    else:
        # Vypočítáme nové EMA pro každou souřadnici.
        return [alpha * new + (1 - alpha) * current for new, current in zip(new_vector, current_ema)]
    

def FIR_filter(new_vector, coefficients):
    """
    Aplikuje FIR (Finite Impulse Response) filtr na vstupní vektor s použitím daných koeficientů.
    
    FIR filtry jsou typ digitálních filtrů, které využívají pevný počet minulých vzorků dat
    pro výpočet nových hodnot. Typicky se používají v aplikacích, kde je důležitá lineární fáze.

    Args:
        new_vector (list of float): Nově příchozí vektor dat, který má být filtrován.
        coefficients (list of float): Koeficienty FIR filtru, které určují vliv jednotlivých
                                      minulých vzorků na výstupní hodnotu.

    Returns:
        list of float: Výstupní filtrovaný vektor, pokud máme dostatek dat; jinak původní vektor.
    """

    # Inicializace historie dat jako statického atributu funkce, pokud ještě neexistuje.
    if not hasattr(FIR_filter, "data_history"):
        FIR_filter.data_history = []

    # Přidání nových dat do historie.
    FIR_filter.data_history.append(new_vector)

    # Omezení délky historie dat na délku koeficientů filtru.
    if len(FIR_filter.data_history) > len(coefficients):
        FIR_filter.data_history.pop(0)
    
    # Pokud nemáme dostatek dat odpovídajících počtu koeficientů, vrátíme vstupní vektor.
    if len(FIR_filter.data_history) < len(coefficients):
        return new_vector  # Nebo vrátit None, pokud ještě nemáme dost dat

    # Inicializace výstupního vektoru nulovými hodnotami.
    num_elements = len(new_vector)
    filtered_vector = [0] * num_elements

    # Počet vzorků v historii dat.
    num_samples = len(FIR_filter.data_history)
    
    # Aplikace FIR filtru na každý prvek vektoru zvlášť.
    for i in range(num_elements):
        sum_val = 0

        # Sumace příspěvků jednotlivých vzorků historie vážených koeficienty.
        for j in range(len(coefficients)):
            sum_val += FIR_filter.data_history[num_samples - j - 1][i] * coefficients[j]
        filtered_vector[i] = sum_val
    
    return filtered_vector


def convert_to_speed_vector(vector, translation_coef, rotation_coef, translation_max_speed, rotation_max_speed):
    """
    Převádí vektor na vektor rychlostí pomocí zadaných koeficientů pro translaci a rotaci.
    
    Args:
        vector (list of int): Vstupní vektor translace a rotace.
        translation_coef (float): Koeficient pro translaci. (0 ≤ tralslation_coef ≤ 1)
        rotation_coef (float): Koeficient pro rotaci. (0 ≤ rotation_coef ≤ 1)
        translation_max_speed (float): Maximální rychlost translace. (-1 ≤ translation_max_speed ≤ 1 [m/sec])
        rotation_max_speed (float): Maximální rychlost rotace. (-pi ≤ translation_max_speed ≤ pi [rad/sec]]
    
    Returns:
        list of float: Vektor rychlostí.
    """

    scale_factor = 1 / (350-DEAD_ZONE_SIZE)
    translation_scale = scale_factor * translation_coef
    rotation_scale = scale_factor * pi * rotation_coef

    for index, value in enumerate(vector):
        if index < 3:
            vector[index] = max(min(value * translation_scale, translation_max_speed), -translation_max_speed)
        else:
            vector[index] = max(min(value * rotation_scale, rotation_max_speed), -rotation_max_speed)

    return vector


def collect_data_tool(file_path):
    """
    Sbírá a ukládá pozici nástroje robota získanou z RTDE rozhraní do CSV souboru.
    Funkce volá metodu rtde_r.getActualTCPPose() pro získání aktuální pozice a 
    následně tuto pozici zapisuje do souboru pomocí funkce write_vector_to_csv.
    """

    # Získání aktuální pozice nástroje robota
    collected_data_tool_position = rtde_r.getActualTCPPose()

    # Zápis pozice do souboru CSV
    write_vector_to_csv(file_path, collected_data_tool_position)


def collect_data_joint(file_path):
    """
    Sbírá a ukládá pozici kloubů robota získanou z RTDE rozhraní do CSV souboru.
    Funkce volá metodu rtde_r.getActualQ() pro získání aktuálních úhlů kloubů a 
    následně tyto úhly zapisuje do souboru pomocí funkce write_vector_to_csv.
    """

    # Získání aktuálních úhlů kloubů robota
    collected_data_joint_position = rtde_r.getActualQ()
    
    # Zápis úhlů do souboru CSV
    write_vector_to_csv(file_path, collected_data_joint_position)



def write_vector_to_csv(file_path, vector):
    """
    Zapisuje vektor do souboru CSV. Každý vektor je přidán na nový řádek.
    
    Args:
        file_path (str): Cesta k souboru CSV.
        vector (list of int): Vektor k zapsání.
    """
        
    # Otevření souboru pro přidávání dat (append mode), takže data nejsou přepsána
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(vector)
