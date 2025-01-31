# SoundOFF Flask API

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Flask

### Installation
1. Clone the repository to your local machine.
2. Navigate to the `espFlaskApi` directory:
    ```sh
    cd espFlaskApi
    ```
3. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```
4. Activate the virtual environment:

    On Linux or macOS:
    ```sh
    source venv/bin/activate
    ```

    On Windows:
    ```sh
    .\venv\Scripts\activate
    ```
5. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the API
1. Ensure the virtual environment is activated.
2. Run the Flask application:
    ```sh
    flask run
    ```
3. The API will be available at `http://127.0.0.1:5000`.

### .env File
The .env file is used to set environment variables for the Flask application. These variables are loaded at runtime and can be used to configure the application. Here is an example of a .env file:

```properties
FLASK_ENV=development
FLASK_APP=app.py
ESP32_SERVER=192.168.1.42
ESP32_PORT=80
API_URL=http://127.0.0.1:5000
DEFAULT_POWER_FACTOR=4.0
```

## 📂 File Descriptions
- `app.py`: The main Flask application file.
- `requirements.txt`: A file containing the list of required Python packages.
- `static/styles.css`: A CSS file for styling the HTML templates.
- `templates/index.html`: The main HTML template file.

## 🛠️ Technical Requirements
- Flask
- Python

## 📞 Support
For any questions or support, please contact the project maintainers.