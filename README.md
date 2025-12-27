# Andhra Pradesh Smart Village Portal 🌱

An IoT-enabled web application designed to help villagers in Andhra Pradesh report environmental issues such as garbage dumping. The system supports real-time issue validation using IoT sensors and helps authorities take timely action.

---

## 📌 Project Overview

Villages often face problems like improper garbage dumping, bad odor, and delayed municipal response. This project provides a **Smart Village Portal** where citizens can report issues online, and IoT sensors are used to confirm and monitor the reported problems.

---

## 🎯 Features

- Citizen login & registration system
- Online issue reporting with image upload
- Location-based issue submission
- Email notifications to citizens and admin
- IoT sensor-based issue validation
- Secure authentication using SQLite & password hashing

---

## 🧠 Part A – Digital Issue Reporting

- Web-based reporting portal using Flask
- User authentication (login & register)
- Issue details: location, description, image
- Data stored in CSV and SQLite database
- Admin receives email with issue image

---

## 🔧 Part B – Sensor-Based Support (IoT)

### Reported Issue:
**Garbage Dumping in Villages**

### Sensors Used:
- Ultrasonic Sensor – detects garbage level
- Gas Sensor (MQ series) – detects bad odor (methane/ammonia)
- IR Sensor – detects human activity near garbage bin
- ESP32 – main controller for data collection
- Motor – controls bin lid or compaction mechanism

### Working Flow:
1. Ultrasonic sensor measures garbage level
2. Gas sensor detects foul smell
3. IR sensor checks human presence
4. ESP32 collects all sensor data
5. Data compared with predefined threshold values
6. If issue confirmed:
   - Motor activates (lid/compactor)
   - Data sent to server/admin
7. Municipal staff receives alert for action

---

## 🛠️ Technologies Used

### Software:
- Python (Flask)
- HTML, CSS, JavaScript
- SQLite Database
- SMTP (Email service)

### IoT Hardware:
- ESP32
- Ultrasonic Sensor
- Gas Sensor (MQ-2 / MQ-135)
- IR Sensor
- Motor (DC / Servo)
- Power Supply

---

## 📂 Project Structure

# Andhra Pradesh Smart Village Portal 🌱

An IoT-enabled web application designed to help villagers in Andhra Pradesh report environmental issues such as garbage dumping. The system supports real-time issue validation using IoT sensors and helps authorities take timely action.

---

## 📌 Project Overview

Villages often face problems like improper garbage dumping, bad odor, and delayed municipal response. This project provides a **Smart Village Portal** where citizens can report issues online, and IoT sensors are used to confirm and monitor the reported problems.

---

## 🎯 Features

- Citizen login & registration system
- Online issue reporting with image upload
- Location-based issue submission
- Email notifications to citizens and admin
- IoT sensor-based issue validation
- Secure authentication using SQLite & password hashing

---

## 🧠 Part A – Digital Issue Reporting

- Web-based reporting portal using Flask
- User authentication (login & register)
- Issue details: location, description, image
- Data stored in CSV and SQLite database
- Admin receives email with issue image

---

## 🔧 Part B – Sensor-Based Support (IoT)

### Reported Issue:
**Garbage Dumping in Villages**

### Sensors Used:
- Ultrasonic Sensor – detects garbage level
- Gas Sensor (MQ series) – detects bad odor (methane/ammonia)
- IR Sensor – detects human activity near garbage bin
- ESP32 – main controller for data collection
- Motor – controls bin lid or compaction mechanism

### Working Flow:
1. Ultrasonic sensor measures garbage level
2. Gas sensor detects foul smell
3. IR sensor checks human presence
4. ESP32 collects all sensor data
5. Data compared with predefined threshold values
6. If issue confirmed:
   - Motor activates (lid/compactor)
   - Data sent to server/admin
7. Municipal staff receives alert for action

---

## 🛠️ Technologies Used

### Software:
- Python (Flask)
- HTML, CSS, JavaScript
- SQLite Database
- SMTP (Email service)

### IoT Hardware:
- ESP32
- Ultrasonic Sensor
- Gas Sensor (MQ-2 / MQ-135)
- IR Sensor
- Motor (DC / Servo)
- Power Supply

---

## 📂 Project Structure
smart-city/
│
├── static/
│ ├── style.css
│ └── smart-city.png
│
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── report.html
│ └── success.html
│
├── uploads/
├── app.py
├── database.db
├── issues.csv
├── requirements.txt
└── README.md


---

## 🚀 How to Run the Project

1. Clone the repository
```bash
git clone https://github.com/your-username/andhra-pradesh-smart-village-portal.git

pip install -r requirements.txt

python app.py

http://127.0.0.1:5000/login


## 🌐Developer Details

Name: Pilla Sreebala Veera Venkata Satyanarayana

Branch: B.Tech – Computer Science & Cyber Security
