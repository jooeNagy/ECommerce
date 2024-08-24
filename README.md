# EndPoints
## Accounts
- Register new account : http://127.0.0.1:8000/api/register/  [POST]
- Authentication & JWT : http://127.0.0.1:8000/api/token/  [POST]
- Show user Info : http://127.0.0.1:8000/api/userinfo/  [GET]
- Update user Info : http://127.0.0.1:8000/api/userinfo/update/  [PUT]
- Forgot password & send Emails : http://127.0.0.1:8000/api/forgot-password/  [POST]
- Reset password : http://127.0.0.1:8000/api/reset-password/<token>  [POST]

## Products
- Show all products & Filters & Pagination : http://127.0.0.1:8000/api/products [GET]
- Show one product : http://127.0.0.1:8000/api/products/5  [GET]
- Add new product : http://127.0.0.1:8000/api/products/new [POST]
- Update product : http://127.0.0.1:8000/api/products/edit/3 [PUT]
- Delete product : http://127.0.0.1:8000/api/products/delete/5 [DELETE]

## Reviews
- Add review : http://127.0.0.1:8000/api/products/reviews/ [POST]
- Delete review : http://127.0.0.1:8000/api/products/reviews/delete/1 [DELETE]

## Orders
- Make new order : http://127.0.0.1:8000/api/orders/new/ [POST]
- Show all orders : http://127.0.0.1:8000/api/orders/ [GET]
- Show one order : http://127.0.0.1:8000/api/orders/13 [GET]
- Update order : http://127.0.0.1:8000/api/orders/process/12/ [PUT]
- Delete order : http://127.0.0.1:8000/api/orders/delete/13/ [DELETE]
