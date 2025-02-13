# FastAPI-Blog

![Image](https://github.com/user-attachments/assets/bbedfc02-2e96-415d-b61b-7f9012f848b8)

---

## 🌟 **Project Goals**

> Blog를 Fast API로 구현하여 Fast API 이해 및 숙련도를 상승시키기.

---

## 🛠️ **Technology Stack**

- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript, Bootstrap5
- **Database**: SQLAlchemy, MySQL

---

## 🖥️ **Getting Started**

Clone the repository and set up locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ChanLim-BD/FastAPI-Blog.git
   ```

2. **Install Dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up the Database**

   ```bash
   docker run --name mysql-container -e MYSQL_ROOT_PASSWORD="What you want" -p 3306:3306 -d mysql:latest
   ```

4. **Containerization: Build**

   ```bash
   docker build -t fastapi-app .
   ```

5. **Containerization: Run**

   ```bash
   docker run -d -p 8081:8081 fastapi-app.
   ```

6. Open your browser and navigate to: `http://<Your IP>:8081/`.

---

## 📷 ScreenShot

![Image](https://github.com/user-attachments/assets/cd4f0473-0080-40f9-925c-a2c3ad595a58)

![Image](https://github.com/user-attachments/assets/197b0052-1739-44e8-a5b3-f9190aa63623)

![Image](https://github.com/user-attachments/assets/46559b77-3235-4d2c-ac60-f8b577eaa7a1)

---

## 🌍 **Future Enhancements**

* CI - Github Action

...