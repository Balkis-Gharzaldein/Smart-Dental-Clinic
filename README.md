# 🦷 Smart Dental Clinic – AI-Enhanced Dental Management System

A comprehensive backend system built with **Django REST Framework** and enhanced with **advanced Artificial Intelligence (AI) capabilities**. It is designed to streamline the management of dental clinics, patients, appointments, panoramic X-ray images, and diagnostic reports.

---

## ✨ Core Technology and Innovation

This project integrates efficient clinical management with the power of Deep Learning, aiming to provide **accurate preliminary diagnoses** from X-ray images, thereby supporting crucial clinical decision-making.

| Core Technology | AI Role | Diagnostic Methodology |
| :--- | :--- | :--- |
| **Django REST Framework** | **Deep Learning (DL)** | **Automatic Semantic Segmentation** of teeth |
| **Python / OpenCV** | **U-Net Model** for Image Segmentation | **Binary Image Analysis & Connected Component Analysis** |
| **PostgreSQL** (Proposed) | **Advanced Image Processing** | **Accurate Diagnostic Measurements** for teeth |

---

## 🚀 Key Features Overview

### 🔐 **User Roles and Access Control (RBAC)**

The system implements Role-Based Access Control to ensure data security and compliance:

* **Clinic Admin (مدير العيادة):**
    * Full system management, including staff (dentists and employees) and appointments.
    * Authority to approve or reject user requests.
* **Dentists (أطباء الأسنان):**
    * Manages patients and appointments.
    * Uploads and analyzes panoramic X-ray images using AI tools.
* **Dental Lab Technicians (فنيو المختبر السني):**
    * Uploads and processes panoramic X-ray images.
    * Applies AI models for image processing and analysis.
* **Patients (المرضى):**
    * Online appointment booking.
    * Uploads personal panoramic X-ray images and views diagnostic reports.

---

## 🧠 AI Methodology and Image Processing

The AI capabilities rely on cutting-edge Deep Learning techniques in medical image processing to achieve highly accurate diagnostics.

### **1. Teeth Semantic Segmentation**

This fundamental step accurately identifies the position and boundaries of each tooth.

* **Model Used:** **U-Net**, a leading Convolutional Neural Network (CNN) architecture for medical image segmentation tasks.
* **Objective:** To achieve accurate **Automatic Semantic Segmentation** of teeth from panoramic radiographic images.
* **Data Training:** Utilizes an anonymized dataset of **116 patients'** panoramic images, scaled to **(512x512)** and trained over **200 Epochs** for optimal results.
* **Post-Processing:** Application of **Connected Component Analysis (CCA)** and **Otsu's Thresholding** to identify connected objects (teeth) and measure their dimensions (length and width) precisely.

### **2. Preliminary Diagnostic Analysis (AI-Powered Diagnostic Features)**

Based on accurate tooth segmentation, the system applies analytical algorithms to identify clinical conditions:

| Req. # | Diagnostic Feature | Technical Methodology |
| :--- | :--- | :--- |
| **1 & 2** | **Caries (Cavities) and Restorations Detection** | **Brightness Analysis** and **Color-Based Masking** in the **HSV** color space. Caries are detected as **dark grey** areas, while restorations appear as highly **bright white** regions. |
| **3** | **Bone Level and Absorption Assessment** | Defining specific Regions of Interest (**ROI**) for the upper and lower jaws, followed by **contrast enhancement** and a color threshold (245) to calculate the **pixel ratio** representing bone density/loss. |
| **4** | **Dental Buds Detection** | Drawing two **semi-circular arcs** (upper and lower) based on empirical coordinates and checking for their intersection with **red (tooth root) pixels** to infer the presence of developing buds. |
| **5** | **Wisdom Teeth Status Detection** | Dividing the image into four quadrants around the center, defining approximate search areas for third molars, and verifying the presence of tooth pixels within these specific regions. |

**For visual confirmation of the results, sample images are available within the project files.**

---

## 🛠️ Technical Environment and Core Libraries

The AI model was built and trained using the following essential libraries:

* **Deep Learning:** ``Tensorflow == 2.4.1``
* **Image Processing:** ``opencv_python == 4.5.1.48``, ``scikit_image == 0.17.2``, ``Imutils == 0.5.4``, ``Pillow == 7.2.0``
* **Numerical & Data Handling:** ``NumPy == 1.19.2``, ``Pandas == 1.1.3``
* **Scientific:** ``Scipy == 1.5.2``

---

## ⚙️ Non-Functional Requirements

| Requirement | Importance and Implementation |
| :--- | :--- |
| **Usability (قابلية الاستخدام)** | Intuitive and efficient interface design for all users, focusing on smooth navigation and visual clarity. |
| **Security (الأمن)** | **Top Priority:** Ensuring the privacy and security of data, especially sensitive X-ray images, through secure protocols and encryption. |
| **Performance (الأداء)** | Capable of efficiently handling a large volume of data and transactions, guaranteeing fast response times and timely completion of real-time image analysis. |
