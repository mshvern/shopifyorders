import requests
import re
import sys
import json


# Getting the date out of an individual comment
def getdate(s):
	pattern = r'(?<=createdAt"\:").+?(?=\"})'
	date = re.findall(pattern, s)
	return date[0]


# Getting the message out of an individual comment
def getmessage(s):
	pattern = r'(?<=message"\:").+?(?=\"\,\"createdAt")'
	message = re.findall(pattern, s)
	return message[0]


def readsettings():
	# Reading AUTH token (API Password in Shopify) and the name of your shop from settings.txt.
	# First line should contain key, while the second one should contain name
	f = open("settings.txt", "r")
	lines = f.read().splitlines()
	url = "https://" + lines[1] + ".myshopify.com/admin/api/graphql.json"
	auth = lines[0]
	# print("auth: " + auth + "'\n url: " + url)
	return (url, auth)


# Main function
def gql():
	# You should use the script with 1 command-line argument (order id),
	# you can get this order ID by going to the url of your order and copying the last part
	if len(sys.argv) < 1 or len(sys.argv) > 2:
		print("Invalid usage of the command! \n Correct usage: python bot.py <order_id>")
		return
	# Getting all the order events
	query = r'{ order(id: "gid://shopify/Product/' + sys.argv[
		1] + '"){events(first: 100){edges{node{__typename message createdAt  }}}}}'

	# Getting settings
	(url, api_token) = readsettings()

	headers = {'X-Shopify-Access-Token': api_token, 'Content-Type': "application/graphql"}

	# posting the request to GraphiQL Shopify API
	r = requests.post(url=url, data=query, headers=headers)

	# searching for the right events from the response
	pattern = r'typename":"CommentEvent".+?(?=\{)'

	found = re.findall(pattern, r.text)

	# basic error handling, should be expanded on/changed if you need to feed the output to another script
	if len(found) < 1:
		print("No matches, details: \n" + r.text)
	dictionary = {}
	index = 0

	# forming a dictionary to dump into json
	for i in found:
		dictionary["Comment " + str(index)] = (getmessage(i), getdate(i))
		index += 1

	# printing out the result to STDOUT
	print(json.dumps(dictionary))


if __name__ == '__main__':
	gql()
