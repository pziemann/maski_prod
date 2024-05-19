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
    cur.execute('SELECT id, size_x, size_y, size_z, color, entry, payment, payment_status, discount, date_of_order, status, payment_received, source_of_order, nickname, description, price, filament_id, amount_used FROM mask_order')
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
        'status': row[10],
        'payment_received': row[11],
        'source_of_order': row[12],
        'nickname': row[13],
        'description': row[14],
        'price': row[15],
        'filament_id': row[16],
        'amount_used': row[17],
    } for row in rows]
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def add_data():
    new_order = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO mask_order (size_x, size_y, size_z, color, entry, payment, payment_status, discount, date_of_order, status, payment_received, source_of_order, nickname, description, price, filament_id, amount_used)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    ''', (
        new_order['size_x'], new_order['size_y'], new_order['size_z'],
        new_order['color'], new_order['entry'], new_order['payment'],
        new_order['payment_status'], new_order['discount'], new_order['date_of_order'],
        new_order['status'], new_order['payment_received'], new_order['source_of_order'],
        new_order['nickname'], new_order['description'], new_order['price'],
        new_order['filament_id'], new_order['amount_used']
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
            discount = %s, date_of_order = %s, status = %s, payment_received = %s, source_of_order = %s,
            nickname = %s, description = %s, price = %s, filament_id = %s, amount_used = %s
        WHERE id = %s
    ''', (
        updated_order['size_x'], updated_order['size_y'], updated_order['size_z'],
        updated_order['color'], updated_order['entry'], updated_order['payment'],
        updated_order['payment_status'], updated_order['discount'], updated_order['date_of_order'],
        updated_order['status'], updated_order['payment_received'], updated_order['source_of_order'],
        updated_order['nickname'], updated_order['description'], updated_order['price'],
        updated_order['filament_id'], updated_order['amount_used'], id
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

@app.route('/api/colours', methods=['GET'])
def get_colours():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, colour_name FROM colour')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    colours = [{'id': row[0], 'colour_name': row[1]} for row in rows]
    return jsonify(colours)

@app.route('/api/colours', methods=['POST'])
def add_colour():
    new_colour = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO colour (colour_name) VALUES (%s) RETURNING id', (new_colour['colour_name'],))
    colour_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': colour_id}), 201

@app.route('/api/colours/<int:id>', methods=['PUT'])
def update_colour(id):
    updated_colour = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE colour SET colour_name = %s WHERE id = %s', (updated_colour['colour_name'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Colour updated successfully'})

@app.route('/api/colours/<int:id>', methods=['DELETE'])
def delete_colour(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM colour WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Colour deleted successfully'})

@app.route('/api/filaments', methods=['GET'])
def get_filaments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT filament.id, filament.size, filament.amount_used, filament.date_of_addition, filament.material, colour.colour_name 
        FROM filament
        JOIN colour ON filament.colour_id = colour.id
    ''')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    filaments = [{'id': row[0], 'size': row[1], 'amount_used': row[2], 'date_of_addition': row[3], 'material': row[4], 'colour_name': row[5]} for row in rows]
    return jsonify(filaments)

@app.route('/api/filaments', methods=['POST'])
def add_filament():
    new_filament = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO filament (colour_id, size, amount_used, material)
        VALUES ((SELECT id FROM colour WHERE colour_name = %s), %s, %s, %s)
        RETURNING id
    ''', (new_filament['colour_name'], new_filament['size'], new_filament['amount_used'], new_filament['material']))
    filament_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': filament_id}), 201

@app.route('/api/filaments/<int:id>', methods=['PUT'])
def update_filament(id):
    updated_filament = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE filament
        SET colour_id = (SELECT id FROM colour WHERE colour_name = %s), size = %s, amount_used = %s, material = %s
        WHERE id = %s
    ''', (updated_filament['colour_name'], updated_filament['size'], updated_filament['amount_used'], updated_filament['material'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Filament updated successfully'})

@app.route('/api/filaments/<int:id>', methods=['DELETE'])
def delete_filament(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM filament WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Filament deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
