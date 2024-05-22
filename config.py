from math import pi

""" USB_initialization """

# Definice Vendor ID a Product ID
VENDOR_ID = 0x256F
PRODUCT_ID = 0xC641


""" UR_initialization """

# IP simulace: 192.168.228.130      IP UR3: 192.168.0.10
UR_IP_ADDRESS = "192.168.228.130"

# Nastavení výchozí polohy UR
DEFAULT_POSITION = [-0.100, -0.180, 0.150, 0.0, 3.14, 0.00]

# EMA filtr koeficient
EMA_COEF = 0.2

# Nastavení koeficientů FIR filtru
FIR_FILTER_COEFS = [0.4, 0.3, 0.15, 0.1, 0.05]

""" UR_control """

# Definice koeficientů pro výpočet rychlostních vektorů pro translaci a rotaci
TRASLATION_COEF = 0.3
ROTATION_COEF = 0.07
TRANSLATION_MAX_SPEED = 0.5    # [m/sec]
ROTATION_MAX_SPEED = pi/8       # [rad/sec]

# Nastavení parametrů filtru pásmové zádrže
DEAD_ZONE_SIZE = 30

# Nastavení parametrů filtru klouzavého průměru
MEMOTY_LENGTH = 5
