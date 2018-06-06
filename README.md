# shopifyorders
Using the new in-development Shopify API to access timeline comments from orders tab. 
There is a stable REST Shopify API, but unfortunately it does not support retrieving timeline (no endpoint for it)
However, there is a new GraphiQL API that DOES support timeline.

The correct usage for this script is "python bot.py <order_id>". 
Where <order_id> is the last part of your order url. 
The script return json in the format of "Comment N" : [message, date].

Before you use the script, you should fill out the settings.txt!
The first line in this file should be the API key you get from your private app
The second line should be the shop name ("SHOPNAME.myshopify.com")
