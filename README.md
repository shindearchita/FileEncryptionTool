# 🔐 File Encryption Tool

## 📌 Overview

File Encryption Tool is a Python-based GUI application designed to securely encrypt and decrypt files using password-based encryption. The application provides a simple user interface while implementing cybersecurity practices such as secure key generation, password strength validation, and activity monitoring.

The project demonstrates practical implementation of data protection concepts, encryption techniques, and secure logging practices.

---

## 🚀 Features

- 🔒 Secure file encryption and decryption
- 🔑 Password-based key generation using SHA-256 hashing
- 🛡️ Password strength checker
- 📋 Secure activity logging
- 🚨 Failed decryption attempt monitoring
- 📂 File selection through graphical interface
- 👁️ Show/Hide password option
- ✅ File validation before encryption
- 🖥️ User-friendly Tkinter GUI

---

## 🛠️ Technologies Used

- **Programming Language:** Python
- **GUI Framework:** Tkinter
- **Encryption Library:** Cryptography (Fernet)
- **Hashing Algorithm:** SHA-256
- **Libraries:**
  - os
  - hashlib
  - base64
  - logging
  - re
  - datetime

---

## 🔐 Security Implementation

### Password-Based Encryption
The application generates a secure encryption key from the user password using SHA-256 hashing and uses Fernet symmetric encryption for protecting files.

### Secure Logging
The application records security events such as:

Sensitive information such as passwords and encryption keys are never stored.

### Failed Access Monitoring

Incorrect decryption attempts are recorded for security monitoring:

---

Learning Outcomes

Through this project, I gained practical experience in:

Symmetric encryption concepts
Password-based security
Cryptographic hashing
Secure logging practices
GUI application development
Basic security monitoring concepts

Developed By

Archita Shinde

Cybersecurity Enthusiast | SOC Analyst Aspirant
