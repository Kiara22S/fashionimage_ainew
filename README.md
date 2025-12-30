# V2 Retail AI: High-Fidelity Fashion Synthesis Engine 👗✨

**V2 Retail AI** is a professional generative AI application designed to automate e-commerce fashion photography. By leveraging the **Gemini 2.5 Flash-Image** model, this tool transforms flat garment designs into studio-quality lifestyle renders, enabling brands to visualize products on diverse models instantly.

---

## 🚀 Key Technical Features

### 1. Nested Batch Processing Architecture
The system is engineered to handle complex catalogs through a multi-layered execution logic:
* **Multi-Color Mapping:** Users can select multiple hex codes or color names, and the system automatically iterates through them.
* **Design Multiplexing:** The engine processes every uploaded design against every selected color. For example, 2 designs × 2 colors = 4 unique renders.

### 2. Smart Canvas & Hemline Protection (Padding Algorithm)
To solve the common "portrait crop" issue where AI models cut off the bottom of garments, I implemented a custom pre-processing step:
* **The Logic:** Using the `Pillow` library, the system calculates the original image dimensions and injects 20% additional vertical white space at the bottom.
* **The Result:** This recalibrates the AI's "camera lens," forcing a full-body or mid-thigh framing that ensures the entire t-shirt or dress is visible.



### 3. Dynamic Prompt Engineering
The backend features a context-aware prompt engine that adapts based on user selection:
* **Gender-Aware Framing:** Different spatial cues are sent to the model for Male, Female, and Kids to account for shoulder-width and height variations.
* **Texture Preservation:** High-detail instructions ensure the AI maintains the integrity of the original design's fabric and print.

### 4. Robust Export System
* **ZIP Archiving:** To bypass browser security restrictions that block multiple simultaneous downloads, I implemented a `zipfile` and `BytesIO` buffer system. This packages all renders into a single high-quality archive.
* **In-Memory Processing:** Images are handled as byte streams, ensuring no temporary files clutter the server environment.

---

## 🛠️ Technical Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Custom CSS for an immersive dark-mode UI)
* **AI Engine:** [Google Gemini 2.5 Flash-Image](https://ai.google.dev/)
* **Image Processing:** [Pillow (PIL)](https://python-pillow.org/)
* **Language:** Python 3.10+
* **Environment:** `python-dotenv` for secure API management

---

## 🏗️ How it Works

1.  **Input:** User uploads flat design files and selects model gender/color palette.
2.  **Preprocessing:** The **Padding Algorithm** adjusts the canvas for professional framing.
3.  **Inference:** The **Prompt Engine** constructs a detailed request for the Gemini 2.5 model.
4.  **Gallery View:** Results are displayed in a responsive grid with individual "Zoom" capabilities.
5.  **Export:** Users download the entire batch as a structured ZIP file.



---

## 📦 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/v2-retail-ai.git](https://github.com/your-username/v2-retail-ai.git)
   cd v2-retail-ai