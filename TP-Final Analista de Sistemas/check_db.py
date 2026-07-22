import pyodbc
import config

conn_str = (
    f"DRIVER={config.DB_DRIVER};"
    f"SERVER={config.DB_SERVER};"
    f"DATABASE={config.DB_NAME};"
    f"Trusted_Connection=yes;"
)
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables:")
    for t in tables:
        print(f" - {t}")
        
    # Check if we can describe Recursos, Operarios, etc.
    for t in ['Recursos', 'Operarios', 'Articulos', 'Relevamientos']:
        if t in tables:
            print(f"\nColumns in {t}:")
            cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{t}'")
            for row in cursor.fetchall():
                print(f"  {row[0]}: {row[1]}")
    conn.close()
except Exception as e:
    print("Error:", e)
