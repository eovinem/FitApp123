import sqlite3 

def criar_banco():

    conn = sqlite3.connect("fitai.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        objetivo TEXT,
        imc REAL,
        treino TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    
)
""")
    
    conn.commit()
    conn.close()

