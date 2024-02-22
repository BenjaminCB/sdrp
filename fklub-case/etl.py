import psycopg2
import pygrametl
import re
import uuid
from pygrametl.tables import CachedDimension, FactTable
from pygrametl.datasources import CSVSource, TransformingSource, HashJoiningSource

conn = psycopg2.connect("dbname=mydatabase user=postgres")
connection = pygrametl.ConnectionWrapper(conn)
connection.setasdefault()

# define dimensions and fact table
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
    attributes=['category', 'type', 'name'],
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

# extract data
category_csv = CSVSource(open('./data/category.csv', 'r'), delimiter=';')

def member_transformer(row):
    row['gender'] = row['gender'] == 'M'
    row['registration_year'] = int(row['year'])

    del row['year']
    del row['active']
    del row['want_spam']
    del row['balance']
    del row['undo_count']

    return row

member_csv = TransformingSource(
    CSVSource(open('./data/member.csv', 'r'), delimiter=';'),
    member_transformer
)

def product_transformer(row):
    del row['active']
    del row['deactivate_date']
    del row['quantity']
    del row['alcohol_content_ml']
    del row['start_date']
    del row['price']
    return row

product_csv = TransformingSource(
    CSVSource(open('./data/product.csv', 'r'), delimiter=';'),
    product_transformer
)

def product_categories_transformer(row):
    del row['id']
    return row

product_categories_csv = TransformingSource(
    CSVSource(open('./data/product_categories.csv', 'r'), delimiter=';'),
    product_categories_transformer
)

room_csv = CSVSource(open('./data/room.csv', 'r'), delimiter=';')

def sale_transformer(row):
    del row['id']
    timestamp = row['timestamp']
    del row['timestamp']
    [date, time] = timestamp.split(' ')
    [year, month, day] = date.split('-')
    row['year'] = int(year)
    row['month'] = int(float(month))
    row['day'] = int(float(day))
    row['hour'] = int(float(time.split(':')[0]))
    # TODO: weekday
    row['weekday'] = 0
    row['price'] = int(row['price'])
    return row

sale_csv = TransformingSource(
    CSVSource(open('./data/sale.csv', 'r'), delimiter=';'),
    sale_transformer
)

# transform data
merge_c_pc = HashJoiningSource(
    src1=category_csv,
    key1='id',
    src2=product_categories_csv,
    key2='category_id'
)

def merge_c_pc_transformer(row):
    row['category'] = row['name']
    del row['name']
    del row['id']
    del row['category_id']

    if row['category'] == 'Events':
        row['type'] = 'other'
    elif row['category'] == 'Spiselige varer':
        row['type'] = 'food'
    else:
        row['type'] = 'drinks'

    return row

trans_merge_c_pc = TransformingSource(merge_c_pc, merge_c_pc_transformer)

merge_p_c_pc = HashJoiningSource(
    src1=product_csv,
    key1='id',
    src2=trans_merge_c_pc,
    key2='product_id'
)

def merge_p_c_pc_transformer(row):
    # regex to remove html tags
    row['product_name'] = re.sub('<[^<]+?>', '', row['name'])
    del row['id']
    del row['name']
    return row

trans_merge_p_c_pc = TransformingSource(merge_p_c_pc, merge_p_c_pc_transformer)

merge_s_r = HashJoiningSource(
    src1=sale_csv,
    key1='room_id',
    src2=room_csv,
    key2='id'
)

def merge_s_r_transformer(row):
    row['room_name'] = row['name']
    del row['id']
    del row['room_id']
    del row['name']
    return row

trans_merge_s_r = TransformingSource(merge_s_r, merge_s_r_transformer)

merge_m_s_r = HashJoiningSource(
    src1=member_csv,
    key1='id',
    src2=trans_merge_s_r,
    key2='member_id'
)

def merge_m_s_r_transformer(row):
    del row['id']
    del row['member_id']
    return row

trans_merge_m_s_r = TransformingSource(merge_m_s_r, merge_m_s_r_transformer)

merge_m_s_r_p_c_pc = HashJoiningSource(
    src1=trans_merge_m_s_r,
    key1='product_id',
    src2=trans_merge_p_c_pc,
    key2='product_id'
)

def merge_m_s_r_p_c_pc_transformer(row):
    del row['product_id']
    return row

trans_merge_m_s_r_p_c_pc = TransformingSource(merge_m_s_r_p_c_pc, merge_m_s_r_p_c_pc_transformer)

# load data
i = 0
for row in trans_merge_m_s_r_p_c_pc:
    i += 1
    if i % 1000 == 0:
        print("Loaded %d of 168142 rows" % i)
    fact_row = {}
    fact_row['member_id'] = memberdim.ensure(row)
    fact_row['room_id'] = roomdim.ensure(row, { 'name': 'room_name' })
    fact_row['product_id'] = productdim.ensure(row, { 'name': 'product_name' })
    fact_row['timestamp_id'] = timestampdim.ensure(row)
    fact_row['price'] = row['price']
    facttbl.ensure(fact_row)

connection.commit()
