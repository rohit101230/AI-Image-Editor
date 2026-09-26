import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from openai import OpenAI
import base64
import io
import os


class AIImageEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("AI Image Editor")
        self.root.geometry("1200x800")
        self.root.minsize(900, 650)

        self.current_image = None
        self.original_image = None
        self.history = []

        # API key is entered by the user during the session.
        self.api_key = ""

        self.setup_ui()

    # =========================================================
    # USER INTERFACE
    # =========================================================

    def setup_ui(self):

        top = tk.Frame(
            self.root,
            bg="#111827",
            height=60
        )
        top.pack(fill="x")
        top.pack_propagate(False)

        title = tk.Label(
            top,
            text="AI IMAGE EDITOR",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#111827"
        )
        title.pack(side="left", padx=20)

        key_button = tk.Button(
            top,
            text="🔑 API Key",
            command=self.enter_api_key,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=7,
            cursor="hand2"
        )
        key_button.pack(side="right", padx=15)

        main = tk.Frame(
            self.root,
            bg="#e5e7eb"
        )
        main.pack(fill="both", expand=True)

        # =====================================================
        # IMAGE AREA
        # =====================================================

        image_frame = tk.Frame(
            main,
            bg="#d1d5db"
        )
        image_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.canvas = tk.Label(
            image_frame,
            text=(
                "Open an image to start\n\n"
                "or generate a new image using a prompt"
            ),
            font=("Segoe UI", 16),
            bg="#f9fafb",
            fg="#6b7280"
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # RIGHT PANEL
        # =====================================================

        panel = tk.Frame(
            main,
            width=330,
            bg="#111827"
        )

        panel.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=15
        )

        panel.pack_propagate(False)

        prompt_title = tk.Label(
            panel,
            text="What do you want to create?",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#111827"
        )

        prompt_title.pack(
            anchor="w",
            padx=20,
            pady=(25, 8)
        )

        self.prompt_box = tk.Text(
            panel,
            height=7,
            font=("Segoe UI", 11),
            wrap="word",
            bg="#1f2937",
            fg="white",
            insertbackground="white",
            relief="flat",
            padx=12,
            pady=12
        )

        self.prompt_box.pack(
            fill="x",
            padx=20
        )

        self.prompt_box.insert(
            "1.0",
            "Draw a realistic duck"
        )

        self.generate_button = tk.Button(
            panel,
            text="✨ GENERATE / EDIT",
            command=self.generate_image,
            font=("Segoe UI", 11, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=10,
            pady=12,
            cursor="hand2"
        )

        self.generate_button.pack(
            fill="x",
            padx=20,
            pady=15
        )

        button_frame = tk.Frame(
            panel,
            bg="#111827"
        )

        button_frame.pack(
            fill="x",
            padx=20
        )

        self.make_button(
            button_frame,
            "📂 Open Image",
            self.open_image
        ).pack(
            fill="x",
            pady=4
        )

        self.make_button(
            button_frame,
            "↩ Undo",
            self.undo
        ).pack(
            fill="x",
            pady=4
        )

        self.make_button(
            button_frame,
            "🔄 Reset",
            self.reset
        ).pack(
            fill="x",
            pady=4
        )

        self.make_button(
            button_frame,
            "💾 Save As",
            self.save_image
        ).pack(
            fill="x",
            pady=4
        )

        examples_title = tk.Label(
            panel,
            text="Try these:",
            font=("Segoe UI", 11, "bold"),
            fg="#d1d5db",
            bg="#111827"
        )

        examples_title.pack(
            anchor="w",
            padx=20,
            pady=(25, 8)
        )

        examples = [
            "Draw a realistic duck",
            "Add a red sports car",
            "Change the background to a beach",
            "Add mountains in the background",
            "Make this look cinematic"
        ]

        for example in examples:

            btn = tk.Button(
                panel,
                text=example,
                command=lambda x=example: self.set_prompt(x),
                font=("Segoe UI", 9),
                bg="#1f2937",
                fg="#d1d5db",
                relief="flat",
                anchor="w",
                padx=10,
                pady=6,
                cursor="hand2"
            )

            btn.pack(
                fill="x",
                padx=20,
                pady=2
            )

        self.status = tk.Label(
            panel,
            text="API key not configured",
            font=("Segoe UI", 9),
            fg="#fbbf24",
            bg="#111827",
            wraplength=280,
            justify="left"
        )

        self.status.pack(
            side="bottom",
            anchor="w",
            padx=20,
            pady=20
        )

    # =========================================================
    # BUTTON HELPER
    # =========================================================

    def make_button(self, parent, text, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg="#374151",
            fg="white",
            relief="flat",
            padx=10,
            pady=9,
            cursor="hand2"
        )

    # =========================================================
    # API KEY
    # =========================================================

    def enter_api_key(self):

        key = simpledialog.askstring(
            "OpenAI API Key",
            "Enter your OpenAI API key:",
            show="*",
            parent=self.root
        )

        if not key:
            return

        key = key.strip()

        self.api_key = key

        self.status.config(
            text="✅ API key loaded for this session.",
            fg="#34d399"
        )

    # =========================================================
    # OPEN IMAGE
    # =========================================================

    def open_image(self):

        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        try:

            image = Image.open(path).convert("RGB")

            self.current_image = image.copy()
            self.original_image = image.copy()
            self.history.clear()

            self.show_image()

            self.status.config(
                text="Image loaded successfully.",
                fg="#34d399"
            )

        except Exception as e:

            messagebox.showerror(
                "Open Error",
                f"Could not open image:\n\n{e}"
            )

    # =========================================================
    # DISPLAY IMAGE
    # =========================================================

    def show_image(self):

        if self.current_image is None:
            return

        image = self.current_image.copy()

        max_width = 750
        max_height = 650

        image.thumbnail(
            (max_width, max_height),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(image)

        self.canvas.configure(
            image=photo,
            text=""
        )

        self.canvas.image = photo

    # =========================================================
    # PROMPT
    # =========================================================

    def set_prompt(self, prompt):

        self.prompt_box.delete(
            "1.0",
            tk.END
        )

        self.prompt_box.insert(
            "1.0",
            prompt
        )

    # =========================================================
    # GENERATE / EDIT
    # =========================================================

    def generate_image(self):

        prompt = self.prompt_box.get(
            "1.0",
            tk.END
        ).strip()

        if not prompt:

            messagebox.showwarning(
                "Missing Prompt",
                "Please enter what you want the AI to create."
            )

            return

        if not self.api_key:

            messagebox.showwarning(
                "API Key Required",
                "Please enter your OpenAI API key first."
            )

            self.enter_api_key()

            if not self.api_key:
                return

        self.generate_button.config(
            state="disabled",
            text="⏳ GENERATING..."
        )

        self.status.config(
            text="AI is generating your image...",
            fg="#60a5fa"
        )

        self.root.update()

        try:

            client = OpenAI(
                api_key=self.api_key
            )

            # =================================================
            # NEW IMAGE
            # =================================================

            if self.current_image is None:

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    input=prompt,

                    tools=[
                        {
                            "type": "image_generation",
                            "model": "gpt-image-2",
                            "size": "1024x1024",
                            "quality": "medium"
                        }
                    ]
                )

            # =================================================
            # EDIT EXISTING IMAGE
            # =================================================

            else:

                image_bytes = io.BytesIO()

                self.current_image.save(
                    image_bytes,
                    format="PNG"
                )

                image_bytes.seek(0)

                base64_image = base64.b64encode(
                    image_bytes.read()
                ).decode("utf-8")

                image_data_url = (
                    "data:image/png;base64,"
                    + base64_image
                )

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": prompt
                                },
                                {
                                    "type": "input_image",
                                    "image_url": image_data_url
                                }
                            ]
                        }
                    ],

                    tools=[
                        {
                            "type": "image_generation",
                            "model": "gpt-image-2",
                            "action": "edit",
                            "size": "1024x1024",
                            "quality": "medium"
                        }
                    ]
                )

            # =================================================
            # GET GENERATED IMAGE
            # =================================================

            generated_image = None

            for item in response.output:

                if item.type == "image_generation_call":

                    generated_image = item.result
                    break

            if not generated_image:

                raise Exception(
                    "OpenAI did not return an image."
                )

            image_bytes = base64.b64decode(
                generated_image
            )

            new_image = Image.open(
                io.BytesIO(image_bytes)
            ).convert("RGB")

            # Save current image for Undo
            if self.current_image is not None:

                self.history.append(
                    self.current_image.copy()
                )

            self.current_image = new_image

            if self.original_image is None:

                self.original_image = new_image.copy()

            self.show_image()

            self.status.config(
                text="✅ Image generated successfully.",
                fg="#34d399"
            )

        except Exception as e:

            error_text = str(e)

            if "insufficient_quota" in error_text.lower():

                error_text = (
                    "This API key does not have enough "
                    "available credits or quota."
                )

            elif "401" in error_text:

                error_text = (
                    "The OpenAI API key appears to be invalid."
                )

            elif "429" in error_text:

                error_text = (
                    "OpenAI rate limit reached. "
                    "Please try again later."
                )

            messagebox.showerror(
                "Generation Error",
                error_text
            )

            self.status.config(
                text="Generation failed. Check the error message.",
                fg="#f87171"
            )

        finally:

            self.generate_button.config(
                state="normal",
                text="✨ GENERATE / EDIT"
            )

    # =========================================================
    # UNDO
    # =========================================================

    def undo(self):

        if not self.history:

            messagebox.showinfo(
                "Undo",
                "Nothing to undo."
            )

            return

        self.current_image = self.history.pop()

        self.show_image()

        self.status.config(
            text="↩ Last change undone.",
            fg="#34d399"
        )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        if self.original_image is None:
            return

        self.current_image = (
            self.original_image.copy()
        )

        self.history.clear()

        self.show_image()

        self.status.config(
            text="🔄 Image reset.",
            fg="#34d399"
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save_image(self):

        if self.current_image is None:

            messagebox.showwarning(
                "Nothing to Save",
                "Generate or open an image first."
            )

            return

        path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("WEBP", "*.webp")
            ]
        )

        if not path:
            return

        try:

            self.current_image.save(path)

            self.status.config(
                text=f"💾 Saved:\n{os.path.basename(path)}",
                fg="#34d399"
            )

            messagebox.showinfo(
                "Saved",
                f"Image saved successfully.\n\n{path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                str(e)
            )


# =============================================================
# START
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AIImageEditor(root)

    root.mainloop()