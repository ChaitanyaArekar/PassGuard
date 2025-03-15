# 🔐 PassGuard - Password Management System

## 📚 Information and Network Security (INS) Mini Project

### 🎯 Project Overview
PassGuard is a secure password management system that helps users generate, store, and manage their passwords safely. The project implements various cryptographic techniques and security measures to ensure the protection of sensitive user data.

### ⭐ Key Features
- **🔒 Secure User Authentication**: User registration and login with encrypted password storage
- **🎲 Password Generator**: 
  - Customizable password generation based on user inputs
  - Multiple encryption options:
    - 🔑 Caesar Cipher (Easy encryption)
    - 🛡️ Rail Fence Cipher (Hard encryption)
- **📋 Password Manager**:
  - 💾 Securely store website credentials
  - 👀 View, edit, and delete saved passwords
  - 🎭 Password masking for enhanced security

### 🛠️ Technologies Used
- **⚙️ Backend**: Python Flask
- **🎨 Frontend**: HTML, CSS, JavaScript
- **🗄️ Database**: MongoDB
- **🔒 Security**:
  - 🔐 Flask-Bcrypt for password hashing
  - 🔑 Flask-Login for session management

### 🚀 Installation & Setup

1. 📥 Clone the repository and navigate to project directory:
   ```bash
   git clone https://github.com/yourusername/PassGuard.git
   cd PassGuard
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt

   # If requirements.txt is not present, use:
   pip install flask flask-bcrypt flask-login pymongo python-dotenv
   ```

4. Create a `.env` file in the root directory:
   ```bash
   # On Windows
   copy nul .env

   # On macOS/Linux
   touch .env
   ```

5. Add environment variables to `.env`:
   ```bash
   # Open .env and add these lines
   SECRET_KEY=your_secret_key_here
   MONGO_URI=mongodb://username:password@host:port/database
   ```

6. Initialize the database:
   ```bash
   # Ensure MongoDB is running on your system
   # For Windows:
   net start MongoDB

   # For macOS/Linux:
   sudo systemctl start mongod
   ```

7. Run the application:
   ```bash
   # Development mode
   python app.py

   # Production mode (using gunicorn, install if not present)
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

8. Access the application:
   - Open your browser and navigate to `http://localhost:5000`
   - Default development server runs on port 5000

### ❗ Troubleshooting
- 🔌 If MongoDB connection fails, ensure the service is running
- ⚙️ Check if all environment variables are properly set
- 🐍 Verify Python version (3.7+ recommended)
- 🔄 For virtual environment issues, delete venv folder and recreate

### 🛡️ Security Features
- 🔒 Encrypted password storage using bcrypt
- 🔑 Session management for secure user authentication
- 🛡️ XSS prevention through template escaping
- 🔐 CSRF protection via Flask-WTF
- 👁️ Secure password masking in the interface

### 📁 Project Structure
```
PassGuard/
├── 📂 static/
│   └── 📂 css/
│       ├── 📄 generator.css
│       ├── 📄 layout.css
│       ├── 📄 login.css
│       └── 📄 manager.css
├── 📂 templates/
│   ├── 📄 base.html
│   ├── 📄 generator.html
│   ├── 📄 login.html
│   └── 📄 manager.html
├── 📄 app.py
├── 📄 .env
└── 📄 README.md
```

### 🔮 Future Enhancements
- 🔄 Additional encryption algorithms
- 📊 Password strength meter
- 🔐 Two-factor authentication
- 🤝 Password sharing capabilities
- 💾 Automated backup system