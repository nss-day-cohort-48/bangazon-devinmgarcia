SELECT 
c.id,
au.first_name || ' ' || au.last_name AS customer_name,
u.first_name || ' ' || u.last_name AS seller_name
FROM bangazonapi_favorite as f
JOIN bangazonapi_customer as c on c.id = f.customer_id
JOIN auth_user as au on c.user_id = au.id
JOIN bangazonapi_customer as ca on ca.id = f.seller_id
JOIN auth_user as u on ca.user_id = u.id;
