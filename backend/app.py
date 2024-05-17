from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DATABASE_HOST'],
        database=os.environ['DATABASE_NAME'],
        user=os.environ['DATABASE_USER'],
        password=os.environ['DATABASE_PASSWORD']
    )
    return conn

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, size_x, size_y, size_z, color, entry, payment, payment_status, discount, date_of_order, finished, payment_received, source_of_order, nickname, description, price FROM mask_order')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    data = [{
        'id': row[0],
        'size_x': row[1],
        'size_y': row[2],
        'size_z': row[3],
        'color': row[4],
        'entry': row[5],
        'payment': row[6],
        'payment_status': row[7],
        'discount': row[8],
        'date_of_order': row[9],
        'finished': row[10],
        'payment_received': row[11],
        'source_of_order': row[12],
        'nickname': row[13],        # New column
        'description': row[14],     # New column
        'price': row[15]            # New column
    } for row in rows]
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def add_data():
    new_order = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO mask_order (size_x, size_y, size_z, color, entry, payment, payment_status, discount, date_of_order, finished, payment_received, source_of_order, nickname, description, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    ''', (
        new_order['size_x'], new_order['size_y'], new_order['size_z'],
        new_order['color'], new_order['entry'], new_order['payment'],
        new_order['payment_status'], new_order['discount'], new_order['date_of_order'],
        new_order['finished'], new_order['payment_received'], new_order['source_of_order'],
        new_order['nickname'], new_order['description'], new_order['price']
    ))
    order_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': order_id}), 201

@app.route('/api/data/<int:id>', methods=['PUT'])
def update_data(id):
    updated_order = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE mask_order
        SET size_x = %s, size_y = %s, size_z = %s, color = %s, entry = %s, payment = %s, payment_status = %s,
            discount = %s, date_of_order = %s, finished = %s, payment_received = %s, source_of_order = %s,
            nickname = %s, description = %s, price = %s
        WHERE id = %s
    ''', (
        updated_order['size_x'], updated_order['size_y'], updated_order['size_z'],
        updated_order['color'], updated_order['entry'], updated_order['payment'],
        updated_order['payment_status'], updated_order['discount'], updated_order['date_of_order'],
        updated_order['finished'], updated_order['payment_received'], updated_order['source_of_order'],
        updated_order['nickname'], updated_order['description'], updated_order['price'], id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Order updated successfully'})

@app.route('/api/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM mask_order WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Order deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
