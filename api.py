from fastapi import FastAPI
import psycopg

app = FastAPI()

conn = psycopg.connect(
    host = 'localhost',
    dbname = 'Music',
    user = 'postgres',
    password = '972279'
)
cursor = conn.cursor()


@app.get("/bands")
def get_bands():
    cursor.execute("SELECT id_band, name_band FROM Bands")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({"id_band": row[0], "name_band": row[1]})
    return result


@app.get("/bands/{id_band}")
def get_band(id_band: int):
    cursor.execute("SELECT id_band, name_band FROM Bands WHERE id_band = %s", (id_band,))
    band = cursor.fetchone()
    if band is None:
        return {"error": "Группа не найдена"}
    return {"id_band": band[0], "name_band": band[1]}