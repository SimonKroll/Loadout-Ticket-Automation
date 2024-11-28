import sqlite3

def initalize(db_path : str):
    
    conn = sqlite3.connect(database=db_path)

    cur = conn.cursor()

    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS "credentials"(
    CardID INTEGER PRIMARY KEY,
    SourceName varchar(127),
    SourceAddress varchar(127),
    SourceAddress2 varchar(127),
    SourcePhone varchar(127),
    Commodity varchar(127),
    ContractNumber varchar(127),
    CustomerName varchar(127),
    CustomerAddress varchar(127),
    CustomerAddress2 varchar(127),
    CustomerCityState varchar(127),
    CarrierName varchar(127),
    TruckPlate varchar(127),
    TrailerPlate varchar(127),
    Notes TEXT
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS "counters"(
    counter_name TEXT PRIMARY KEY,
    value INTEGER
    )''')

    cur.execute('''INSERT OR IGNORE INTO counters (counter_name, value) VALUES 
    ('loadID', 0),
    ('contractID', 0);''')



    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()