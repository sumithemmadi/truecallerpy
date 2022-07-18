<h1 id="truecallerpy">
    <a href="https://github.com/sumithemmadi/truecallerpy">Truecallerpy</a>
</h1>

[![PyPI - Implementation](https://img.shields.io/pypi/v/truecallerpy?style=flat-square)](https://pypi.org/project/truecallerpy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/truecallerpy?style=flat-square)](https://pypi.org/project/truecallerpy)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/truecallerpy?style=flat-square)](https://pypistats.org/packages/truecallerpy)
[![PyPI - License](https://img.shields.io/pypi/l/truecallerpy?style=flat-square)](https://github.com/sumithemmadi/truecallerpy/edit/main/LICENSE.md)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fsumithemmadi%2Ftruecallerpy.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fsumithemmadi%2Ftruecallerpy?ref=badge_shield)


<p>A  package to search phone number details.</p>


# Requirements

* Valid Mobile Number(Phone number verification for truecaller)
* [Truecaller InstallationId](https://github.com/sumithemmadi/truecallerpy#InstallationId)

## [Command Line Usage](https://github.com/sumithemmadi/truecallerpy)

### Installation

Install this pip package

```bash
pip install truecallerpy
```

### Login

Then  login to your truecaller account .

```bash
~$ truecallerpy --login
```

> If you get any error try running '**sudo truecallerpy --login**'. If you are using Windows try the command with **Adminitrative Privilege**.

> If you still facing problems in login then try below steps.

   1. On Truecaller Android, tap on the 3 line menu on top left then click on `setting's`.
   2. Tap on `Privacy Center` and then click on `Download my data`.
   3. Now a json file is downloaded. 
   4. Save the json file on your PC at any location e.g /home/HP/1234567890-99123456789.json
   5. On you terminal or command prompt enter below command.
   ```
   ~$ truecallerpy --login -f /home/HP/1234567890-99123456789.json
   ```
   6. Now you are successfully logged in.


### InstallationId

Enter the below command to see your **InstallationId**.

```bash
~$ truecallerpy --installationid
```

Print only installation Id.

```bash
~$ truecallerpy -i -r
```

### Searching a number

```bash
~$ truecallerpy -s [number]
```

```yaml
{
   "data": [
      {
         "id": "jsiebejebbeebhee/dnss00w==",
         "name": "Sumith Emmadi",
         "imId": "1g7rm006b356o",
         "gender": "UNKNOWN",
         "image": "https://storage.googleapis.com/tc-images-noneu/myview/1/jdvdidbdhvdjdvddbkdbeiebeieb",
         "score": 0.9,
         "access": "PUBLIC",
         "enhanced": true,
         "phones": [
            {
               "e164Format": "+000000000000",
               "numberType": "MOBILE",
               "nationalFormat": "+000000000000",
               "dialingCode": 91,
               "countryCode": "IN",
               "carrier": "Airtel",
               "type": "openPhone"
            }
         ],
         "addresses": [
            {
               "city": "Andhra Pradesh",
               "countryCode": "IN",
               "timeZone": "+05:30",
               "type": "address"
            }
         ],
         "internetAddresses": [
            {
               "id": "email@gmail.com",
               "service": "email",
               "caption": "Sumith Emmadi",
               "type": "internetAddress"
            }
         ],
         "badges": [
            "verified",
            "user"
         ],
         "cacheTtl": "",
         "sources": [],
         "searchWarnings": [],
         "surveys": []
      }
   ],
   "provider": "ss-nu",
   "stats": {
      "sourceStats": []
   }
}
```

To get raw output.

```bash
~$ truecallerpy -s [number] -r
{"data":[{"id":"jsiebejebbeebhee/dnss00w==","name":"Sumith Emmadi","imId":"1g7rm006b356o","gender":"UNKNOWN","image":"https://storage.googleapis.com/tc-images-noneu/myview/1/jdvdidbdhvdjdvddbkdbeiebeieb","score":0.9,"access":"PUBLIC","enhanced":true,
"phones":[{"e164Format":"+000000000000","numberType":"MOBILE","nationalFormat":"+000000000000","dialingCode":91,"countryCode":"IN","carrier":"Airtel","type":"openPhone"}],"addresses":[{"city":"Andhra Pradesh","countryCode":"IN","timeZone":"+05:30","type":"address"}],
"internetAddresses":[{"id":"email@gmail.com","service":"email","caption":"Sumith Emmadi","type":"internetAddress"}],"badges":["verified","user"],"cacheTtl":"","sources":[],"searchWarnings":[],"surveys":[]}],"provider":"ss-nu","stats":{"sourceStats":[]}}
```


To print only name.

```bash
~$ truecallerpy -s [number] --name
Name : Sumith Emmadi
```

Other command's

```bash
~$ truecallerpy -s [number] -r --name

Sumith Emmadi
```

To print only email.

```bash
~$ truecallerpy -s [number] --email
Email : username@email.com
```

Other command's

```bash
~$ truecallerpy -s [number] --email -r 

username@email.com
```


#### To get only JSON output

```bash
~$ truecallerpy -s [number] --json
```
```bash
~$ truecallerpy -s [number] -r --json
{"data":[{"id":"jsiebejebbeebhee/dnss00w==","name":"Sumith Emmadi","imId":"1g7rm006b356o","gender":"UNKNOWN","image":"https://storage.googleapis.com/tc-images-noneu/myview/1/jdvdidbdhvdjdvddbkdbeiebeieb","score":0.9,"access":"PUBLIC","enhanced":true,
"phones":[{"e164Format":"+000000000000","numberType":"MOBILE","nationalFormat":"+000000000000","dialingCode":91,"countryCode":"IN","carrier":"Airtel","type":"openPhone"}],"addresses":[{"city":"Andhra Pradesh","countryCode":"IN","timeZone":"+05:30","type":"address"}],
"internetAddresses":[{"id":"email@gmail.com","service":"email","caption":"Sumith Emmadi","type":"internetAddress"}],"badges":["verified","user"],"cacheTtl":"","sources":[],"searchWarnings":[],"surveys":[]}],"provider":"ss-nu","stats":{"sourceStats":[]}}
```

### To make a bulk search 

```
~$ truecallerpy --bs [Numbers seperated by comma]
```

```
Example : 
 ~$ truecallerpy --bs 9912345678,+14051234567,+919987654321
```


## Usage 

```python
from truecallerpy import search_phonenumber

id = "Your installationId at here"
# To know your installation id run `truecallerpy -i` on terminal or command prompt

# search_phonenumber( "PHONE_NUMBER","COUNTRY_CODE","INSTALLATION_ID")

search_phonenumber("9912345678","IN", id)

# ==> search_phonenumber("+12093031250","IN", id)

```

* **PHONE_NUMBER** : Number you want to search.
* **COUNTRY_CODE** : Country code you want to use by default . If mobile number is not in **E164**(International Format) Format then **COUNTRY_CODE** will be considered as a country code of that Mobile Number.
* **INSTALLATION_ID** : To know your InstallationId , install the package globally.

## Bulk search


```python
from truecallerpy import search_phonenumber,bulk_search

id = "your installation id"
# To know your installation id run `truecallerpy -i` on terminal or command prompt

# bulk_search( "DATA","COUNTRY_CODE","INSTALLATION_ID") 

data = "9912345678,+14051234567,+919987654321" # phone numbers seperated by commas

bulk_search(data,"IN", id)
```
* **DATA** : Numbers seperated by commas.

## License

MIT License

Copyright (c) 2022 Emmadi Sumith Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
