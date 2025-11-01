import rsa

# Cargar clave pública del remitente 
with open("clave_publica.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Cargar mensaje y firma 
with open("mensaje.txt", "rb") as f:
    mensaje = f.read()

with open("firma.bin", "rb") as f:
    firma = f.read()

# Verificar la firma digital 
try:
    rsa.verify(mensaje, firma, public_key)
    print(" La firma es válida. El mensaje proviene del remitente auténtico.")
except rsa.VerificationError:
    print(" La firma no es válida. El mensaje pudo haber sido alterado.")

#  Mostrar el mensaje decodificado 
print(" Mensaje recibido:", mensaje.decode('utf-8'))
