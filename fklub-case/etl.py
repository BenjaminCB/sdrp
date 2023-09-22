import psycopg2
import pygrametl
from pygrametl.tables import CachedDimension, FactTable
from pygrametl.datasources import CSVSource, MergeJoiningSource

conn = psycopg2.connect("dbname=mydatabase user=postgres")
connection = pygrametl.ConnectionWrapper(conn)
connection.setasdefault()

memberdim = CachedDimension(
    name='member',
    key='member_id',
    attributes=['registration_year', 'gender'],
)

roomdim = CachedDimension(
    name='room',
    key='room_id',
    attributes=['name', 'description'],
)

productdim = CachedDimension(
    name='product',
    key='product_id',
    attributes=['category', 'type' 'name'],
)

timestampdim = CachedDimension(
    name='timestamp',
    key='timestamp_id',
    attributes=['hour', 'day', 'month', 'year', 'weekday'],
)

facttbl = FactTable(
    name='sales',
    keyrefs=['member_id', 'room_id', 'product_id', 'timestamp_id'],
    measures=['price'],
    targetconnection=connection
)

category_csv = CSVSource(open('./data/category.csv', 'r'), delimiter=';')
member_csv = CSVSource(open('./data/member.csv', 'r'), delimiter=';')
product_csv = CSVSource(open('./data/product.csv', 'r'), delimiter=';')
product_categories_csv = CSVSource(open('./data/product_categories.csv', 'r'), delimiter=';')
room_csv = CSVSource(open('./data/room.csv', 'r'), delimiter=';')
sale_csv = CSVSource(open('./data/sale.csv', 'r'), delimiter=';')


