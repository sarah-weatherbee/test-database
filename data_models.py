from sqlalchemy import create_engine, MetaData, Column, Integer, Numeric, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Set up connection between sqlalchemy and postgres dbapi
engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/fakedata"
)

# Create a metadata object
metadata = MetaData()

# (postgres schema) for accounts, items, stores, and transactions
accounts_table = Table(
  "accounts",
  metadata,
Column("account_id", Integer, primary_key=True),
Column("first_name", String(35), nullable=False),
Column("last_name", String(35), nullable=False)
)

transactions_table = Table(
  "transactions",
  metadata,
Column("trans_id", Integer, primary_key=True),
Column("trans_date", Date, nullable=False),
Column("trans_disc", Numeric, nullable=False),
Column("trans_amt", Numeric(10,2), nullable=False)
)

items_table = Table(
  "items",
  metadata,
Column("item_id", Integer, primary_key=True),
Column("item_cat", String(35), nullable=False),
Column("date_added_inv", Date, nullable=False),
Column("item_disc", Numeric, nullable=False),
Column("sale_price", Numeric(10,2), nullable=False),
Column("account_id", ForeignKey ("accounts.account_id"), nullable=False),
Column("trans_id", ForeignKey ("transactions.trans_id"), nullable=False)
)


# Start transaction to commit DDL to postgres database
with engine.begin() as conn:
    metadata.create_all(conn)
    # Log the tables as they are created
    for table in metadata.tables.keys():
        print(f"{table} successfully created")