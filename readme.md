# references:

# digest 
https://y0m0r.hateblo.jp/entry/20130324/1364122853
failed due to: 
ModuleNotFoundError: No module named 'django.utils.importlib' 
when running 'python manage migrate'
tried to solve, but the source code seems to be outdated.

Then, I tried to implement digest authentication mannually.
I tried to use Postman to test.
At first, with only input of username and password, i failed because "Authentication" is not shown in request header.
I played around a bit and then realized two field are mandatory, which are realm and nonce. 
Their values are not important, but they have to be present.

# inventory
Table inventory with columns product (name) and quantity (amount)
The product "sales" is used to store total profit since the last deletion. After deletion, its quantity is reset to 0. 
sales/10000 is the actual profit, this is because "sales" is saved as an integer, but we want it as float with 2dc.
