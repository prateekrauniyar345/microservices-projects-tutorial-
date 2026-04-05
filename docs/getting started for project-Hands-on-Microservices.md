To get started with this microservices project and see it running, follow these steps:

---

## **1. Prerequisites**
Ensure you have the following installed on your system:
- **Python 3.x**: Required for running the Flask application.
- **Docker**: For containerizing and running the services.
- **Docker Compose**: For orchestrating the services.
- **Git**: To manage the repository (if needed).

---

## **2. Clone the Repository**
If you don’t already have the repository, clone it:
```bash
git clone <repository-url>
cd Hands-on-Microservices-with-Python
```

---

## **3. Install Dependencies**
### **Option 1: Using Docker (Recommended)**
- The project is already containerized, so you don’t need to install Python dependencies manually.
- Proceed to the **Run the Application** section.

### **Option 2: Without Docker**
If you want to run the application locally without Docker:
1. Navigate to the `app/` directory:
   ```bash
   cd app
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## **4. Run the Application**

### **Option 1: Using Docker Compose**
1. Start the Docker containers:
   ```bash
   docker-compose up
   ```
   This will:
   - Build the Docker image for the `frontend` service.
   - Start the `frontend` service on port `80`.

2. Access the application:
   - Open your browser and go to `http://localhost`.

3. To stop the application:
   ```bash
   docker-compose down
   ```

### **Option 2: Without Docker**
1. Navigate to the `app/` directory:
   ```bash
   cd app
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Access the application:
   - Open your browser and go to `http://127.0.0.1:5000`.

---

## **5. Test the Application**
- Use the browser to navigate through the application (e.g., login, register, browse products, place orders).
- Use the provided Postman collection (`docs/api/postman/order-system.postman_collection.json`) to test the APIs:
  1. Import the collection into Postman.
  2. Use the environment file (`Packt Order Management - Dev.postman_environment.json`) to set up API variables.

---

## **6. Debugging and Logs**
- **Docker Logs**:
  To view logs for the running containers:
  ```bash
  docker-compose logs
  ```
- **Flask Debug Mode**:
  If running locally, the Flask app is already in debug mode (`debug=True` in `app.py`).

---

## **7. Deployment**
For production deployment:
1. Use `docker-compose.deploy.yml` to deploy all services (frontend, product, user, order, and their databases).
2. Run:
   ```bash
   docker-compose -f docker-compose.deploy.yml up
   ```

---

Let me know if you encounter any issues or need further assistance!