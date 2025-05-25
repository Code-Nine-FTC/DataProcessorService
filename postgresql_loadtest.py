# mypy: ignore-errors
import asyncio
import os
import time

import asyncpg

DB_URL = os.getenv("DATABASE_POSTGRES_URL")

NUM_INSERCOES = 10000
BATCH_SIZE = 500  # insere 500 por vez


async def preparar_banco(conn):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id SERIAL PRIMARY KEY,
            station_id INT,
            valor FLOAT,
            timestamp TIMESTAMPTZ DEFAULT now()
        );
    """)


async def inserir_dados(conn):
    inicio = time.time()

    for i in range(0, NUM_INSERCOES, BATCH_SIZE):
        batch = [(j, 42.0) for j in range(i, i + BATCH_SIZE)]
        await conn.executemany(
            "INSERT INTO sensor_data (station_id, valor) VALUES ($1, $2);",
            batch
        )

    fim = time.time()
    print(f"Inseridos {NUM_INSERCOES} registros em {fim - inicio:.2f} segundos")


async def main():
    conn = await asyncpg.connect(DB_URL)
    await preparar_banco(conn)
    await inserir_dados(conn)
    await conn.close()


asyncio.run(main())
