CREATE TABLE mask_order (
    id SERIAL PRIMARY KEY,
    size_x FLOAT,
    size_y FLOAT,
    size_z FLOAT,
    color VARCHAR(50),
    entry VARCHAR(50),
    payment VARCHAR(50),
    payment_status VARCHAR(50),
    discount INT DEFAULT 0,
    date_of_order DATE,
    finished BOOLEAN,
    payment_received BOOLEAN,
    source_of_order VARCHAR(100),
    nickname VARCHAR(50),          -- New column
    description TEXT,              -- New column
    price FLOAT                    -- New column
);

INSERT INTO mask_order (size_x, size_y, size_z, color, entry, payment, payment_status, discount, date_of_order, finished, payment_received, source_of_order, nickname, description, price) 
VALUES (10.5, 20.3, 30.2, 'Red', 'Entry1', 'Credit Card', 'Paid', 5, '2024-05-16', TRUE, TRUE, 'OLX', 'orzel1n', 'Detailed long description', 350);

INSERT INTO mask_order (size_x, size_y, size_z, color, entry, payment, payment_status, discount, date_of_order, finished, payment_received, source_of_order, nickname, description, price) 
VALUES (15.5, 25.3, 35.2, 'Blue', 'Entry2', 'PayPal', 'Pending', 10, '2024-05-17', FALSE, FALSE, 'OLX', 'dzesica21', 'Detailed long description 2', 335);
