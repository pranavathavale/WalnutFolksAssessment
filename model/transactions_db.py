import psycopg2
import os

DATABASE_URL = os.environ["DATABASE_URL"]

def get_connection():
    return psycopg2.connect(DATABASE_URL)


def insert_transaction(payload):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transactions (
            transaction_id,
            source_account,
            destination_account,
            amount,
            currency,
            status,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (transaction_id) DO NOTHING;
    """, (
        payload["transaction_id"],
        payload["source_account"],
        payload["destination_account"],
        payload["amount"],
        payload["currency"],
        "PROCESSING"
    ))

    conn.commit()
    cur.close()
    conn.close()


def update_transaction_processed(transaction_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE transactions
        SET status = 'PROCESSED',
            processed_at = NOW()
        WHERE transaction_id = %s
          AND status = 'PROCESSING';
    """, (transaction_id,))

    conn.commit()
    cur.close()
    conn.close()


def fetch_transaction(transaction_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT transaction_id,
               source_account,
               destination_account,
               amount,
               currency,
               status,
               created_at,
               processed_at
        FROM transactions
        WHERE transaction_id = %s;
    """, (transaction_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "transaction_id": row[0],
        "source_account": row[1],
        "destination_account": row[2],
        "amount": float(row[3]),
        "currency": row[4],
        "status": row[5],
        "created_at": row[6],
        "processed_at": row[7]
    }
