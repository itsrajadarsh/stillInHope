# StillInHope – Report Generator 📝

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://stillinhope.onrender.com)

StillInHope is a simple Flask web application where users can report local issues like **potholes** or **roadside garbage**.  
It instantly generates a **certificate PDF** with details (name, location, date/time, disaster type, and photo), shows a **preview image**, and lets users **download & share** the report.  

---

## 🚀 Features
- Upload a photo of an issue (pothole, garbage, broken streetlight, etc.).
- Auto-generate a **certificate PDF** with:
  - Reporter name  
  - Disaster/issue type  
  - Location  
  - Timestamp  
  - Uploaded photo + PM/CM image (from template)  
- View & download both:
  - PDF report  
  - JPEG preview image (optimized for smaller size)  
- Mobile-friendly:
  - Can **take a photo** or **upload from gallery**  
- **Smooth UX**:
  - Spinner + friendly "Please wait" message while generating  
  - Auto-scrolls to the generated preview after processing  
- Optional **tweet helper**:
  - Generates ready-to-post tweet text (user manually attaches downloaded media).  
- Auto-refresh pings the server every 10 minutes to keep the free Render service awake.  

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)  
- **PDF Editing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) + [Pillow (PIL)](https://python-pillow.org/)  
- **Frontend**: HTML, JavaScript, Bootstrap  
- **Deployment**: [Render](https://render.com/)  

---

## 📦 Installation (Local Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsrajadarsh/stillInHope.git
   cd stillinhope
