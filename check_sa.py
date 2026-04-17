import urllib.request
import json

URL = "https://tgcpyatrllswhlysqfer.supabase.co/rest/v1/super_admins?select=*"
HEADERS = {
    "apikey": "sb_publishable_lwmxiQPF5yUSQnDu4JK12A_mN4tMdWH",
    "Authorization": "Bearer sb_publishable_lwmxiQPF5yUSQnDu4JK12A_mN4tMdWH"
}

req = urllib.request.Request(URL, headers=HEADERS)
with urllib.request.urlopen(req) as response:
    print(response.read().decode())
