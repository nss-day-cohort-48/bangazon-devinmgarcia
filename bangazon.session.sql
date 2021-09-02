SELECT
p.name,
p.description,
p.price
FROM bangazonapi_product as p
WHERE p.price < 1000
