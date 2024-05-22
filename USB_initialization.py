import usb.core
from config import VENDOR_ID, PRODUCT_ID

# Inicializace USB zařízení pomocí VendorID a ProductID
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

# Kontrola, zda bylo zařízení úspěšně nalezeno
if device is None:
    raise ValueError(f"Zařízení s Vendor ID {VENDOR_ID} a Product ID {PRODUCT_ID} nebylo nalezeno!")
else:
    print("Zařízení nalezeno:", device)

# Odpojení jádrového ovladače, pokud je aktivní, aby mohl být použit custom driver
if device.is_kernel_driver_active(0):
    try:
        device.detach_kernel_driver(0)
        print("Kernel driver odpojen")
    except usb.core.USBError as e:
        print(f"Kernel driver nemohl být odpojen: {e}")

# Nastavení konfigurace zařízení
device.set_configuration()

# Nastavení endpointu zařízení pro čtení dat
endpoint = device[0][(0, 0, 0)][0]
