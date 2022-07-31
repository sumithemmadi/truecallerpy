from truecallerpy import search_phonenumber,bulk_search

id = "your installation id"
# To know your installation id run `truecallerpy -i` on terminal or command prompt

# bulk_search( "DATA","COUNTRY_CODE","INSTALLATION_ID") 

data = "9912345678,+14051234567,+919987654321" # phone numbers seperated by commas

bulk_search(data,"IN", id)