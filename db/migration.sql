DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'colour') THEN
        CREATE TABLE colour (
            id SERIAL PRIMARY KEY,
            colour_name VARCHAR(50) UNIQUE NOT NULL
        );

        -- Insert default colours
        INSERT INTO colour (colour_name) VALUES ('black'), ('pink'), ('lavender'), ('blue'), ('yellow'), ('green');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'filament') THEN
        CREATE TABLE filament (
            id SERIAL PRIMARY KEY,
            colour_id INT NOT NULL,
            size FLOAT NOT NULL,
            amount_used FLOAT DEFAULT 0,
            date_of_addition DATE DEFAULT CURRENT_DATE,
            material VARCHAR(50) NOT NULL,
            FOREIGN KEY (colour_id) REFERENCES colour(id)
        );
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name='mask_order' AND column_name='filament_used'
    ) THEN
        ALTER TABLE mask_order ADD COLUMN filament_used INT REFERENCES filament(id) DEFAULT NULL;
    END IF;
END $$;
