FJMC TEACHING BOARD - WINDOWS STARTER + LIVEKIT SERVER SETUP

WINDOWS APP (PC par)
1) Node.js LTS install karein: https://nodejs.org/
2) Is folder mein CMD kholen (folder address bar mein cmd type karke Enter).
3) Commands:
   npm install
   npm start
   Board Electron window mein khulega.
4) Installer banane ke liye:
   npm run dist
   Installer dist folder mein milega.

NOTE: Electron wrapper aapka board HTML desktop window mein kholta hai. Ye PeerJS live ko LiveKit mein automatically migrate nahi karta.

LIVEKIT VPS DEPLOY (Ubuntu VPS; production domain + TLS recommended)
1) VPS par Docker install karein aur firewall/security group mein ports kholen:
   TCP 7880 (signal/API; TLS proxy ke peeche), TCP 7881 (RTC TCP),
   UDP 50000-60000 (RTC media). UDP 7882 optional/depending on config.
2) livekit folder mein livekit.yaml.example ko livekit.yaml naam se copy karein.
3) API key/secret ko long random secrets se replace karein. Public secret share na karein.
4) livekit folder mein:
   docker compose up -d
5) Server ko internet par production use karne ke liye official LiveKit deployment guide,
   domain, TLS (typically 443 via reverse proxy), firewall, public IP/NAT configuration zaroor karein.

TOKEN SERVICE (sample; production mein auth + HTTPS + rate limits zaroor)
1) livekit folder mein CMD/terminal:
   npm install
2) LIVEKIT_API_KEY aur LIVEKIT_API_SECRET environment variables set karein, phir:
   npm start
3) POST /token JSON: {"room":"class-1","identity":"teacher-1"}
   Ye sample token service scaffold hai. Board ke PeerJS live UI ko LiveKit SDK/token endpoint
   ke saath code-level integrate karna abhi baaki hai.

Official docs: https://docs.livekit.io/transport/self-hosting/deployment/
