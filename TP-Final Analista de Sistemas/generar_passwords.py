import bcrypt
from database import get_db_cursor

# 1. Generamos los hashes criptográficos REALES para tus contraseñas
# Usamos .encode('utf-8') porque bcrypt trabaja con bytes
hash_jefe = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
hash_metodista = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print("Hashes reales calculados:")
print(f"Jefe: {hash_jefe}")
print(f"Metodista: {hash_metodista}")

# 2. Actualizamos la base de datos usando tu propio Context Manager
try:
    # commit=True asegura que los cambios se guarden en la base de datos
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("UPDATE Usuarios SET password_hash = ? WHERE username = 'jefe'", (hash_jefe,))
        cursor.execute("UPDATE Usuarios SET password_hash = ? WHERE username = 'metodista'", (hash_metodista,))
        
    print("\n¡Éxito! Las contraseñas en SQL Server han sido reemplazadas por hashes válidos.")
except Exception as e:
    print(f"\nHubo un error al actualizar la base de datos: {e}")