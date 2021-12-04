from sqlalchemy import create_engine, MetaData, select
from faker import Faker
import sys
import random


# Connect between sqlalchemy and postgres dbapi
engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/fakedata"
)

metadata = MetaData()

faker = Faker()

with engine.connect() as conn:
    metadata.reflect(conn)

#create table data
accounts = metadata.tables["accounts"]
transactions = metadata.tables["transactions"]
items = metadata.tables["items"]


item_cat_list = ["hat", "shirt", "sweater", "vest", "cardigan", "dress",
                 "jeans", "pants", "skirt", "athletic", "shoes", "coat", "earrings", "ring", "necklace"]

trans_disc_list = ["0", ".10", "25", "10"]

item_disc_list = ["0", ".25", ".50", ".75"]

class GenerateData:
  def __init__(self):
    self.table = sys.argv[1]
    self.num_records = int(sys.argv[2])

  def create_data(self):
      if self.table not in metadata.tables.keys():
          return print(f"{self.table} does not exist")

      if self.table == "accounts":
         with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = accounts.insert().values(
                        first_name=faker.first_name(),
                        last_name=faker.last_name()
                    )
                    conn.execute(insert_stmt)

      if self.table == "transactions":
            with engine.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = transactions.insert().values(
                        trans_date=faker.date_between_dates(date_start=2019-11-1, date_end=2021-11-1),
                        # trans_disc=random.choice(trans_disc_list),
                        trans_disc=faker.random_int(),
                        trans_amt=faker.random_int(10, 10000) / 100.0
                    )
                conn.execute(insert_stmt)

      if self.table == "items":
            with engine.begin() as conn:
                for _ in range(self.num_records):

                    insert_stmt = items.insert().values(
                        item_cat=random.choice(item_cat_list),
                        date_added_inv = faker.date_between_dates(date_start=2019-5-1, date_end=2019-10-29),
                        item_disc=random.choice(item_disc_list),
                        sale_price=faker.random_int(10, 100),
                        account_id=random.choice(conn.execute(select([accounts.c.account_id])).fetchall())[0],
                        trans_id=random.choice(conn.execute(select([transactions.c.trans_id])).fetchall())[0]
                    )
                conn.execute(insert_stmt)

if __name__ == "__main__":
    generate_data = GenerateData()
    generate_data.create_data()
