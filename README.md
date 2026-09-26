# AI Image Editor

A Python-based AI Image Editor that generates and edits images using natural-language prompts.

Instead of using complicated editing tools, users can simply describe what they want to create or change, and the application uses AI image generation to produce the result.

## ✨ Features

* 🖼️ Open existing images
* ✨ Generate images using natural-language prompts
* 🎨 Edit existing images using AI
* 🔑 Users can enter their own API key
* ↩️ Undo changes
* 🔄 Reset to the original image
* 💾 Save edited images
* 🖥️ Simple desktop interface built with Python and Tkinter

## 🧠 How It Works

The application follows a simple workflow:

**User Prompt → AI Image Model → Generated/Edited Image → Preview → Save**

For example, a user can enter:

> Draw a realistic yellow duck sitting on grass.

Or, after opening an existing image:

> Add mountains in the background.

The application sends the request to the configured AI image-generation service and displays the resulting image.

## 🛠️ Technologies Used

* Python
* Tkinter
* Pillow (PIL)
* OpenAI API
* Base64 image processing
* Git & GitHub

## 📁 Project Structure

```text
AI-Image-Editor/
│
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── test_output.png
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rohit101230/AI-Image-Editor.git
```

### 2. Open the project folder

```bash
cd AI-Image-Editor
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install the required packages

```bash
pip install -r requirements.txt
```

## 🔑 API Key

The application requires the user's own API key to generate or edit images.

Click:

**🔑 API Key**

inside the application and enter your API key when prompted.

### Security

**Never upload your real API key to GitHub.**

The project uses `.gitignore` to prevent the local `.env` file from being uploaded.

Do not share your API key publicly or place it directly inside `main.py`.

## ▶️ Run the Application

After installing the dependencies, run:

```bash
python main.py
```

The AI Image Editor window will open.

## 🖼️ Example Prompts

Try prompts such as:

```text
Draw a realistic yellow duck sitting on grass.
```

```text
Add a red sports car.
```

```text
Change the background to a beach.
```

```text
Add mountains in the background.
```

```text
Make this image look cinematic.
```

## 🎯 Project Goal

The goal of this project is to explore how natural-language AI can make image creation and editing simpler for everyday users.

Instead of requiring users to learn complex image-editing tools, the application allows them to describe the desired result using ordinary language.

## 🚀 Future Improvements

Planned improvements include:

* Better image-editing controls
* More advanced prompt handling
* Image selection and editing regions
* Improved UI/UX
* Image generation history
* Drag-and-drop image support
* Windows `.exe` version
* Easier distribution for non-technical users

## 👨‍💻 Author

**Rohit Rawat**

Built as a practical project exploring the intersection of:

**AI + Image Generation + Python + Business/Product Thinking**

## ⭐ Feedback

If you find the project interesting, feel free to explore the code, try it out, and share feedback.
