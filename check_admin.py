import urllib.request
import json

ORG_ID = "org_e6847dd3-1099-45ca-8870-9057a356b929"
URL = f"https://tgcpyatrllswhlysqfer.supabase.co/rest/v1/admin?organization_id=eq.{ORG_ID}&select=*"
HEADERS = {
    "apikey": "sb_publishable_lwmxiQPF5yUSQnDu4JK12A_mN4tMdWH",
    "Authorization": "Bearer sb_publishable_lwmxiQPF5yUSQnDu4JK12A_mN4tMdWH"
}

req = urllib.request.Request(URL, headers=HEADERS)
with urllib.request.urlopen(req) as response:
    print(response.read().decode())
