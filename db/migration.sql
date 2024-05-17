DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name='mask_order' AND column_name='source_of_order'
    ) THEN
        ALTER TABLE mask_order ADD COLUMN source_of_order VARCHAR(100);
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name='mask_order' AND column_name='nickname'
    ) THEN
        ALTER TABLE mask_order ADD COLUMN nickname VARCHAR(50);
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name='mask_order' AND column_name='description'
    ) THEN
        ALTER TABLE mask_order ADD COLUMN description TEXT;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name='mask_order' AND column_name='price'
    ) THEN
        ALTER TABLE mask_order ADD COLUMN price FLOAT;
    END IF;

END $$;


