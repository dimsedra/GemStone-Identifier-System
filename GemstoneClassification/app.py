import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json

# Set up page config
st.set_page_config(page_title="Gemstone Expert System", page_icon="💎", layout="centered")

st.title("💎 Gemstone Classification Expert System")
st.write("Identifikasi batu permata menggunakan Model AI Visual (Computer Vision) atau berdasarkan Ciri Fisik (Sistem Pakar).")

tab1, tab2, tab3 = st.tabs(["📷 Mode Visual (Gambar)", "🔍 Mode Sistem Pakar (Fisik)", "🧠 Mode Hibrida (Visual + Fisik)"])

@st.cache_resource
def load_model():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    with open("classes.json", "r") as f:
        classes = json.load(f)
        
    num_classes = len(classes)
    
    model = models.resnet18(weights=None)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    try:
        model.load_state_dict(torch.load("gemstone_model.pth", map_location=device))
        model = model.to(device)
        model.eval()
        return model, classes, device
    except Exception as e:
        st.error(f"Failed to load model: {e}. Please ensure 'gemstone_model.pth' is in the directory.")
        return None, None, None

@st.cache_data
def load_knowledge_base():
    try:
        with open("knowledge_base.json", "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load knowledge base: {e}")
        return {}

model, classes, device = load_model()
kb = load_knowledge_base()

with tab1:
    if model:
        uploaded_file = st.file_uploader("Upload a Gemstone Image", type=["jpg", "png", "jpeg"], key="upload_tab1")
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file).convert("RGB")
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Uploaded Gemstone", use_column_width=True)
            
            # Preprocess
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
            ])
            
            image_tensor = transform(image).unsqueeze(0).to(device)
            
            with col2:
                st.subheader("Visual Analysis:")
                with st.spinner("Analyzing properties..."):
                    with torch.no_grad():
                        outputs = model(image_tensor)
                        # Apply softmax to get probabilities
                        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                        
                    # Get top 5 predictions
                    top_prob, top_classid = torch.topk(probabilities, 5)
                    
                    # Show results with progress bars for probabilities
                    for i in range(5):
                        class_name = classes[top_classid[i].item()]
                        prob = top_prob[i].item() * 100
                        st.write(f"**{class_name}** - {prob:.2f}%")
                        st.progress(int(prob))
                    
                    st.success(f"**💡 Penjelasan Ahli:** Berdasarkan rona warna, pola, dan struktur kristal yang dianalisis oleh Komputer Visi, model sangat yakin ({top_prob[0].item() * 100:.1f}%) bahwa batu ini adalah **{classes[top_classid[0].item()]}**. Karakteristik visualnya selaras dengan kelas ini dibandingkan yang lainnya.")

with tab2:
    st.subheader("🔍 Sistem Pakar (Analisis Fisik)")
    st.markdown("Masukkan karakteristik fisik batu Anda jika diketahui. Sistem akan mengalkulasi kecocokan berdasarkan rentang mutlaknya.")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        mohs_input = st.slider("Kekerasan (Mohs)", 1.0, 10.0, 7.0, 0.1, key="mohs_tab2")
    with col_b:
        ri_input = st.number_input("Refractive Index (RI)", min_value=1.00, max_value=3.00, value=1.54, step=0.01, key="ri_tab2")
    with col_c:
        sg_input = st.number_input("Specific Gravity (SG)", min_value=1.00, max_value=8.00, value=2.65, step=0.01, key="sg_tab2")
        
    if st.button("Analisis Karakteristik", key="btn_tab2"):
        if kb:
            with st.spinner("Menghitung probabilitas dengan Mesin Inferensi..."):
                scores = []
                for gem_name, props in kb.items():
                    mohs_diff = min(abs(props["mohs"] - mohs_input) / 3.0, 1.0)
                    ri_diff = min(abs(props["ri"] - ri_input) / 0.3, 1.0)
                    sg_diff = min(abs(props["sg"] - sg_input) / 1.5, 1.0)
                    
                    total_deviation = (mohs_diff * 0.4) + (ri_diff * 0.3) + (sg_diff * 0.3)
                    certainty = max(0.0, (1.0 - total_deviation) * 100)
                    scores.append((gem_name, certainty))
                    
                scores.sort(key=lambda x: x[1], reverse=True)
                
                st.markdown("### Hasil Analisis Pakar:")
                for i in range(5):
                    name, prob = scores[i]
                    st.write(f"**{name}** - Tingkat Keyakinan: {prob:.2f}%")
                    st.progress(int(prob))
                    
                top_name, top_cert = scores[0]
                kb_props = kb.get(top_name, {})
                if kb_props:
                    st.success(f"**💡 Penjelasan Ahli:** Sistem memilih **{top_name}** sebagai prediksi tertinggi ({top_cert:.1f}%). Input Anda sangat sesuai dengan standar laboratorium, di mana {top_name} aslinya memiliki kekerasan **{kb_props.get('mohs')} Mohs** (vs input {mohs_input}), Indeks Bias **{kb_props.get('ri')}** (vs input {ri_input}), dan Berat Jenis **{kb_props.get('sg')}** (vs input {sg_input}).")
        else:
            st.error("Knowledge base tidak tersedia.")

with tab3:
    st.subheader("🧠 Mode Hibrida (Fusion Visual + Fisik)")
    st.markdown("Unggah gambar dan masukkan karakteristik fisik batu untuk mendapatkan prediksi gabungan (Ensemble).")
    
    if model and kb:
        uploaded_hybrid = st.file_uploader("Upload Gemstone Image (Diperlukan)", type=["jpg", "png", "jpeg"], key="upload_tab3")
        
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            mohs_hybrid = st.slider("Kekerasan (Mohs)", 1.0, 10.0, 7.0, 0.1, key="mohs_tab3")
        with col_y:
            ri_hybrid = st.number_input("Refractive Index (RI)", min_value=1.00, max_value=3.00, value=1.54, step=0.01, key="ri_tab3")
        with col_z:
            sg_hybrid = st.number_input("Specific Gravity (SG)", min_value=1.00, max_value=8.00, value=2.65, step=0.01, key="sg_tab3")
            
        if uploaded_hybrid is not None:
            if st.button("Jalankan Inferensi Fusion", key="btn_tab3"):
                # Display image
                image = Image.open(uploaded_hybrid).convert("RGB")
                st.image(image, caption="Uploaded Gemstone", use_column_width=False, width=300)
                
                with st.spinner("Menghitung Prediksi AI dan Parameter Fisik..."):
                    # 1. Computer Vision Calculation
                    transform = transforms.Compose([
                        transforms.Resize((224, 224)),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                             std=[0.229, 0.224, 0.225])
                    ])
                    image_tensor = transform(image).unsqueeze(0).to(device)
                    
                    with torch.no_grad():
                        outputs = model(image_tensor)
                        probabilities_cv = torch.nn.functional.softmax(outputs[0], dim=0)
                    
                    cv_scores_dict = {}
                    for idx, class_name in enumerate(classes):
                        cv_scores_dict[class_name] = probabilities_cv[idx].item() * 100

                    # 2. Expert System Calculation
                    expert_scores_dict = {}
                    for gem_name, props in kb.items():
                        mohs_diff = min(abs(props["mohs"] - mohs_hybrid) / 3.0, 1.0)
                        ri_diff = min(abs(props["ri"] - ri_hybrid) / 0.3, 1.0)
                        sg_diff = min(abs(props["sg"] - sg_hybrid) / 1.5, 1.0)
                        
                        total_deviation = (mohs_diff * 0.4) + (ri_diff * 0.3) + (sg_diff * 0.3)
                        certainty = max(0.0, (1.0 - total_deviation) * 100)
                        expert_scores_dict[gem_name] = certainty
                        
                    # 3. Fusion (50% CV + 50% Expert System)
                    final_scores = []
                    for class_name in classes:
                        cv_val = cv_scores_dict.get(class_name, 0.0)
                        ex_val = expert_scores_dict.get(class_name, 0.0)
                        # Rata-rata terbobot
                        final_val = (cv_val * 0.5) + (ex_val * 0.5)
                        final_scores.append((class_name, final_val))
                        
                    # Sort by highest final confidence
                    final_scores.sort(key=lambda x: x[1], reverse=True)
                    
                    st.markdown("### 🏆 Hasil Keputusan Hibrida (Top 5):")
                    for i in range(5):
                        name, final_prob = final_scores[i]
                        # Tampilkan juga detail perpecahan probabilitas
                        cv_detail = cv_scores_dict.get(name, 0.0)
                        ex_detail = expert_scores_dict.get(name, 0.0)
                        st.write(f"**{name}** - Kesimpulan Akhir: {final_prob:.2f}% (Visual: {cv_detail:.1f}%, Pakar: {ex_detail:.1f}%)")
                        st.progress(int(final_prob))
                        
                    top_hybrid_name, top_hybrid_prob = final_scores[0]
                    cv_v = cv_scores_dict.get(top_hybrid_name, 0.0)
                    ex_v = expert_scores_dict.get(top_hybrid_name, 0.0)
                    
                    if cv_v > 85 and ex_v > 85:
                        reason = "karena pola visual maupun susunan sifat fisiknya saling mendukung dan amat cocok secara persentase probabilitas."
                    elif cv_v > ex_v:
                        reason = f"mengingat meskipun input parameter fisiknya meleset/punya tingkat kesesuaian sedang ({ex_v:.1f}%), rupa fisiknya divisualisasikan sangat meyakinkan ({cv_v:.1f}%) sehingga mendominasi bobot kalkulasi."
                    else:
                        reason = f"mengingat meskipun AI kurang yakin dengan wujud gambarnya ({cv_v:.1f}%), uji karakteristik fisik yang Anda inputkan sangat presisi menunjang ciri-ciri mutlak batu tersebut ({ex_v:.1f}%)."
                        
                    st.success(f"**💡 Penjelasan Ahli (Hybrid Reasoning):** Sistem menyimpulkan ini kemungkinan adalah **{top_hybrid_name}** dengan probabilitas akhir **{top_hybrid_prob:.1f}%**. Inferensi ini ditarik {reason}")
    else:
        st.warning("Tunggu sampai model sistem selesai dimuat.")
