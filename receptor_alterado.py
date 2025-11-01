import rsa

#  1. Cargar clave pública del remitente 
with open("clave_publica.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

#  2. Cargar mensaje y firma originales 
with open("mensaje.txt", "rb") as f:
    mensaje_original = f.read()

with open("firma.bin", "rb") as f:
    firma = f.read()

#  3. Verificar el mensaje original 
print("🔹 Verificando mensaje original:")
try:
    rsa.verify(mensaje_original, firma, public_key)
    print(" La firma es válida. El mensaje no fue alterado.\n")
except rsa.VerificationError:
    print(" La firma no es válida en el mensaje original.\n")

#  4. Simular un mensaje alterado 
mensaje_alterado = b"Autorizo el acceso al sistema (modificado por alguien)"

#  5. Verificar el mensaje alterado 
print("Verificando mensaje alterado:")
try:
    rsa.verify(mensaje_alterado, firma, public_key)
    print(" Firma válida (esto no debería pasar).")
except rsa.VerificationError:
    print(" Firma no válida. El mensaje fue modificado y la verificación falla.\n")

#  6. Mostrar ambos mensajes 
print(" Mensaje original  :", mensaje_original.decode('utf-8'))
print(" Mensaje alterado :", mensaje_alterado.decode('utf-8'))
