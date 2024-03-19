INSERT INTO 
    checkout_attribution
SELECT
    checkout_id,
    user_id,
    product_id,
    quantity,
    total_amount,
    payment_method,
    payment_status,
    payment_description,
    gender,
    category,
    profit,
    source,
    checkout_timestamp,
    click_timestamp
FROM 
    (
        SELECT
            co.checkout_id,
            u.user_id,
            co.product_id,
            co.quantity, 
            p.price * co.quantity * co.discount as total_amount,
            co.payment_method,
            co.payment_status,
            co.payment_description,
            u.gender,
            p.category,
            (p.price * co.quantity * co.discount - co.shipping_cost) * p.commission_rate AS profit,
            cl.source,
            co.checkout_timestamp,
            cl.click_timestamp,
            ROW_NUMBER() OVER (
                PARTITION BY cl.user_id
                ORDER BY cl.click_timestamp
            ) AS rn
        FROM
            checkouts AS co
            JOIN users FOR SYSTEM_TIME AS OF co.processing_timestamp AS u ON co.user_id = u.user_id
            JOIN products FOR SYSTEM_TIME AS OF co.processing_timestamp AS p ON co.product_id = p.product_id
            LEFT JOIN clicks AS cl ON co.user_id = cl.user_id
            AND co.checkout_timestamp BETWEEN cl.click_timestamp
            AND cl.click_timestamp + INTERVAL '1' HOUR
    )
WHERE 
    rn = 1;