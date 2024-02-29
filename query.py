import sqlite3


# SQL query to execute
query = """
SELECT
    b.number,
    SUM(t.value) AS total_volume_ether
FROM
    transactions t
        JOIN
    blocks b ON t.block_hash = b.hash
WHERE
    b.timestamp >= '2024-01-01 00:00:00'
    AND b.timestamp <= '2024-01-01 00:30:00'
GROUP BY
    b.number
ORDER BY
    total_volume_ether DESC
LIMIT 1;
"""


def execute_result_query(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        # Fetch and display the result
        result = cursor.fetchone()
        if result:
            print(f"Block Number: {result[0]} has the maximum volume of ether transferred with a value of: {result[1]}")
        else:
            print("No results found for the specified time range.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection to the database
        conn.close()
