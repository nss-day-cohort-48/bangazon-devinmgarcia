<<<<<<< HEAD
select o.id,
u.first_name || ' ' || u.last_name as full_name,
sum(p.price) as order_total,
count(op.id) as num_items
from bangazonapi_order as o
join bangazonapi_customer as c on c.id = o.customer_id
join auth_user as u on u.id = c.user_id
left join bangazonapi_orderproduct as op on op.order_id = o.id
left join bangazonapi_product as p on op.product_id = p.id
where o.payment_type_id NOTNULL
group by o.id
=======
SELECT 
c.id,
au.first_name || ' ' || au.last_name AS customer_name,
u.first_name || ' ' || u.last_name AS seller_name
FROM bangazonapi_favorite as f
JOIN bangazonapi_customer as c on c.id = f.customer_id
JOIN auth_user as au on c.user_id = au.id
JOIN bangazonapi_customer as ca on ca.id = f.seller_id
JOIN auth_user as u on ca.user_id = u.id;
>>>>>>> main
