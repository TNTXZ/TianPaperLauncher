import requests
def check():
    header = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36"
                }
    requests.get("http://www.tianqi.eu.org/download/version.txt", headers=header)
    version = ""
    local_version = ""
    with open("version.txt",mode="r",encoding="utf-8") as f:
        version = float(f.read())
        f.close
    with open("local_version.txt",mode="r",encoding="utf-8") as f:
        local_version = float(f.read())
        f.close
    if version != local_version:
        requests.get("http://www.tianqi.eu.org/download/" + str(version) + ".exe", headers=header)

