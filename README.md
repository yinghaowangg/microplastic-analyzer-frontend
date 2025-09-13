Microplastic Analyzer: An AI-Powered Image Analysis Platform

An integrated platform for microplastic detection, segmentation, and characterization, powered by YOLOv8 segmentation, a Flask backend, and a React (Vite) frontend.
This project demonstrates how AI can be applied to environmental monitoring by enabling automatic identification, quantification, and visualization of microplastic particles in complex real-world samples.

✨ Features
	•	📤 Image Upload: Supports microscope/fluorescence image input
	•	🔍 YOLOv8-Seg Detection: Automatic detection and segmentation of microplastic particles
	•	📊 Visualization: Dynamic doughnut chart and counts for detected PP and PS particles
	•	🧾 Automated Report Generation: Summary of detection results, with potential environmental and health implications
	•	🌐 Full-Stack Architecture: React + Vite frontend, Flask backend, API-driven communication

📂 Project Structure

microplastic-analyzer/
 ├── backend/               # Flask + YOLO backend
 │   ├── app.py             # Main API entry
 │   ├── utils/             # Utility scripts
 │   │   ├── image_processor.py
 │   │   ├── report_generator.py
 │   │   └── ...
 │   ├── static/results/    # YOLO prediction outputs
 │   └── requirements.txt   # Python dependencies
 │
 ├── frontend/              # React + Vite frontend
 │   ├── src/pages/         # App pages
 │   │   ├── UploadPage.jsx
 │   │   └── ReportPage.jsx
 │   ├── src/styles/        # CSS styles
 │   └── package.json       # Node dependencies
 │
 ├── runs/                  # YOLO training logs (ignored in git)
 └── README.md

⚙️ Setup

Frontend (React + Vite)

cd frontend
npm install
npm run dev

Backend (Flask + YOLOv8)

cd backend
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python app.py

	•	Backend runs at: http://localhost:5001
	•	Frontend runs at: http://localhost:5173

⸻

Usage
	1.	Open the frontend in your browser
	2.	Upload a microscope image
	3.	The YOLO model automatically detects and segments microplastic particles
	4.	View statistics (counts per class, total number) in real time
	5.	Read the auto-generated analysis report

⸻

 Model Information
	•	Framework: YOLOv8n-seg
	•	Dataset: 300 manually annotated fluorescence microplastic images
	•	Classes:
	•	PP (Polypropylene) → class 1
	•	PS (Polystyrene) → class 2
	•	Training: 100 epochs
	•	Performance: mAP50 ≈ 0.99

⸻

 Example

Detection Result

⸻

📌 Roadmap
	•	Extend support to additional classes (PET, PE, PVC, PA)
	•	Integrate spectral feature simulation for enhanced classification
	•	Deploy demo online (Render + GitHub Pages) for public access
	•	Batch image analysis and exportable reports

⸻

 License

This project is released under the MIT License.

⸻

👤 Author: Yinghao Wang
🎓 Trinity College Dublin · Computer Science & Business
🌱 Research focus: Hyperspectral imaging and microplastic detection

⸻

✨ With this project, I aim to bridge AI-driven image analysis and environmental engineering applications, showcasing how deep learning can accelerate microplastic monitoring and risk assessment.

⸻
