import cv2
from deepface import DeepFace
from tkinter import Tk, Button, Label, filedialog, messagebox
from PIL import Image, ImageTk
import os

class AgeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("人脸年龄识别")
        self.image_label = Label(master)
        self.image_label.pack(pady=10)

        self.upload_btn = Button(master, text="上传图片", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.save_btn = Button(master, text="保存识别结果", command=self.save_image, state='disabled')
        self.save_btn.pack(pady=5)

        self.processed_img = None  # 保存处理后的 OpenCV 图像

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return

        img = cv2.imread(path)

        try:
            results = DeepFace.analyze(img, actions=['age'], enforce_detection=False)

            if not isinstance(results, list):
                results = [results]

            for result in results:
                age = result['age']
                region = result['region']  # {'x': int, 'y': int, 'w': int, 'h': int}

                # 绘制人脸框
                x, y, w, h = region['x'], region['y'], region['w'], region['h']
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # 构造显示文本：年龄信息
                text = f"Age: {int(age)}"
                cv2.putText(img, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            # 保存图像
            self.processed_img = img

            # 显示图像
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            pil_img = pil_img.resize((400, 300))
            self.tk_image = ImageTk.PhotoImage(pil_img)
            self.image_label.config(image=self.tk_image)
            self.save_btn.config(state='normal')

        except Exception as e:
            messagebox.showerror("识别失败", str(e))
            self.processed_img = None
            self.image_label.config(image='')
            self.save_btn.config(state='disabled')


    def save_image(self):
        if self.processed_img is None:
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg")],
                                                 title="保存识别图像")
        if save_path:
            cv2.imwrite(save_path, self.processed_img)
            messagebox.showinfo("保存成功", f"图像已保存到:\n{save_path}")

if __name__ == "__main__":
    root = Tk()
    app = AgeApp(root)
    root.mainloop()
