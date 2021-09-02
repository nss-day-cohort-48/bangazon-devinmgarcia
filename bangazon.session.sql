SELECT 
o.id,
u.first_name || ' ' || u.last_name,
sum(p.price) as order_total,
pt.merchant_name
FROM bangazonapi_order as o
LEFT JOIN bangazonapi_customer as c on c.id = o.customer_id
LEFT JOIN auth_user as u on u.id = c.user_id
LEFT JOIN bangazonapi_orderproduct as op on op.order_id = o.id
left join bangazonapi_product as p on op.product_id = p.id
LEFT JOIN bangazonapi_payment as pt on o.payment_type_id = pt.id
where o.payment_type_id NOTNULL
GROUP BY o.id
