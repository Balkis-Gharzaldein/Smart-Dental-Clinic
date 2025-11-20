# 🦷 Smart Dental Clinic – AI-Enhanced Dental Management System

A backend system built with **Django REST Framework** and **AI capabilities** for managing dental clinics, patients, appointments, X-ray images, and reports.  
This system supports multiple user roles with role-based access control and integrates AI for dental image analysis.

---

## 🚀 Features Overview

### 🔐 **User Roles**
- **Clinic Admin**
  - Full access to the clinic system  
  - Manages dentists and staff  
  - Approves or rejects requests

- **Dentists**
  - Manage patients and appointments  
  - Upload and analyze dental X-ray images (panoramic)  

- **Dental Lab Technicians**
  - Upload, process, and annotate X-ray images  

- **Patients**
  - Book appointments  
  - Upload panoramic images  
  - View personal info and reports  

---

## 📌 Functional Requirements

### **AI-Powered Features**
| Req. # | Description |
|--------|------------|
| 1 | Detect dental caries (cavities) |
| 2 | Detect pre-existing restorations (crowns, bridges, etc.) |
| 3 | Assess bone level and absorption |
| 4 | Detect dental buds for children |
| 5 | Detect wisdom teeth status |

### **Clinic Admin Features**
| Req. # | Description |
|--------|------------|
| 6 | Login to the system |
| 7 | Manage dentists and staff |
| 8 | Manage appointments |
| 9 | Manage panoramic X-ray images |
| 10 | View clinic statistics |

### **Dentist Features**
| Req. # | Description |
|--------|------------|
| 11 | Login to the system |
| 12 | View patients |
| 13 | Manage appointments |
| 14 | Upload panoramic images |

### **Dental Lab Technician Features**
| Req. # | Description |
|--------|------------|
| 15 | Login to the system |
| 16 | Upload X-ray panoramic images |
| 17 | Process images using AI models |

### **Patient Features**
| Req. # | Description |
|--------|------------|
| 18 | Book appointments |
| 19 | Upload panoramic X-ray images |
| 20 | View personal information |
| 21 | Process panoramic images |
| 22 | Store personal data and media |

---

## ⚙️ Non-Functional Requirements

| Requirement | Description |
|-------------|------------|
| **Usability** | Intuitive interface for users with different experience levels. Smooth navigation, attractive colors, and logical layout. |
| **Security** | Ensures privacy and security of user data. Uses secure protocols for data transfer and encrypts sensitive data (especially X-ray images). |
| **Performance** | Handles a large number of users and transactions efficiently. Fast response to user inputs and timely task completion. |

---
