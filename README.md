# ARCHINT // OSINT TERMINAL

A web-based **OSINT-style terminal interface** built using **Python Flask** and a custom **HTML/JS terminal frontend**.
The project simulates an intelligence terminal capable of running commands for news lookup, IP geolocation, and market simulation.

---

## Features

* Terminal-style user interface
* Real-time news lookup
* IP geolocation lookup
* Simulated stock market with ASCII candlestick charts
* Animated terminal typing effects
* Fullscreen terminal mode

---

## Tech Stack

Frontend

* HTML
* CSS
* JavaScript

Backend

* Python
* Flask

APIs

* NewsData API
* IP-API Geolocation

---

## Project Structure

```
archint/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
|   └── API-KEY.txt
│
└── README.md
```

---



| Command           | Description                  |
| ----------------- | ---------------------------- |
| `NEWS [query]`    | Fetch real-time news         |
| `STOCKS [symbol]` | Simulated stock market chart |
| `IP [address]`    | IP geolocation lookup        |
| `DEV`             | View developer profile       |
| `CC`              | Show command menu            |
| `CLS`             | Clear terminal               |

Example:

```
NEWS technology
IP 8.8.8.8
STOCKS AAPL
```

---

## Deployment

This project is deployed using:

* Render


## Security Notice

The stock data in this project is **simulated** and intended for educational purposes only.

---

## Author

GVR
Hack Club Member
Interested in building creative tech projects and exploring cybersecurity.

---

## License

This project is for **educational and experimental purposes**.
