import rsa

#1. Generar las claves (solo una vez) ===
public_key, private_key = rsa.newkeys(512)

# Guardar las claves en archivos
with open("clave_publica.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

with open("clave_privada.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))

print(" Claves generadas y guardadas en archivos.")

#  Crear y firmar el mensaje ===
mensaje = "Autorizo el acceso al sistema".encode('utf-8')

# Firmar con la clave privada
firma = rsa.sign(mensaje, private_key, "SHA-256")

# Guardar mensaje y firma
with open("mensaje.txt", "wb") as f:
    f.write(mensaje)

with open("firma.bin", "wb") as f:
    f.write(firma)

print("Mensaje y firma guardados para enviar al receptor.")
