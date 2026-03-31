# 💎 Gemstone Classification Expert System

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-CV_Model-ee4c2c)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

An end-to-end intelligent system that identifies and classifies 87 different types of gemstones. This application goes beyond traditional Computer Vision (CV) by integrating a **Hybrid Expert System** that fuses deep learning image classification with rule-based scientific mineralogy (Mohs Hardness, Refractive Index, and Specific Gravity).

## ✨ Features

- **📷 Visual Classification (Computer Vision)**: Leverages a fine-tuned **ResNet18** model to classify gemstones directly from uploaded images.
- **🔍 Physical Expert System (Rule-based)**: An inference engine that calculates probabilistic matches based purely on physical characteristics (Mohs, RI, SG) against a built-in Knowledge Base.
- **🧠 Hybrid Inference (Fusion Ensemble)**: Combines the predictive power of the neural network with the exactness of the physical rule-based system (50:50 weighted average) to provide highly confident, combined predictions.
- **💡 Explainable AI (XAI)**: A built-in reasoning facility (Transparent Reasoning) that acts like a gemologist, presenting human-readable justifications and insights on *why* a particular gemstone was chosen as the top prediction.
- **🌐 Interactive Web UI**: A sleek, user-friendly interface built with **Streamlit**.

## 🚀 Tech Stack

- **Machine Learning**: PyTorch, TorchVision (ResNet18)
- **Web App**: Streamlit
- **Data Processing**: PIL, Pandas/NumPy
- **Knowledge Base**: JSON

## 📋 Prerequisites

- Python 3.8 or higher
- A CUDA-enabled GPU (optional but recommended for faster inference/training)

## 🛠️ Installation & Setup

1. **Clone the repository** (if applicable) and navigate to the project directory:
   ```bash
   git clone https://github.com/yourusername/gemstone-expert-system.git
   cd gemstone-expert-system
   ```

2. **Install Dependencies**
   It's recommended to create a virtual environment, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Knowledge Base Generation**
   Generate or update the `knowledge_base.json` database used by the Expert System engine:
   ```bash
   python generate_kb.py
   ```

## 🖥️ Usage

### 1. Running the Web Application (Streamlit)
To start the interactive interface, run the following command:
```bash
python -m streamlit run app.py
```
The application will launch on `http://localhost:8501`. From there, you can explore the three unique tabs: Visual Mode, Physical Mode, and Hybrid Mode.

### 2. Training the Model (Optional)
If you wish to retrain the ResNet18 model on a custom dataset or fine-tune it further:
```bash
python train.py
```
*Note: Make sure your images are structured properly inside the `dataset/train` and `dataset/test` folders.*

### 3. Command Line Prediction (Optional)
To run a quick prediction directly from your terminal:
```bash
python predict.py path/to/your/image.jpg
```

## 🗃️ Knowledge Base
The system utilizes a structured JSON dataset (`knowledge_base.json`) derived from gemological laboratories. It maps 87 gemstone classes to their standard average values:
- **Mohs Hardness**: Resistance to scratching (1.0 - 10.0 scale).
- **Refractive Index (RI)**: How light propagates through the gem.
- **Specific Gravity (SG)**: The density of the gem compared to water.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 
Feel free to open an issue or submit a Pull Request if you'd like to improve the Knowledge Base accuracy or the CV model.

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
