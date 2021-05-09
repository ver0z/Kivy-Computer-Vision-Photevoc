from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from PIL import Image as PilImage
from PIL import ImageEnhance
import cv2
from kivy.graphics.texture import Texture
import numpy as np
import os


root_kv = """
WindowManager:
    MainWindow:
    SecondWindow:

<MainWindow>:
    name: "main"
    id: pri
    canvas:
        Rectangle:
            source: 'img/entrada.jpg'
            size: self.width, self.height

    Button:
        text: "Open"
        size_hint: 0.166, 0.075
        pos_hint: {"center_x": .5, "center_y": .3}
        on_release:
            app.root.current = "second"
            root.manager.transition.direction = "left"
            app.file_manager_open()



<SecondWindow>:
    name: "second"
    id: sec
    canvas.before:
        Color:
            rgba: 22/255, 103/255, 168/255, 1
        Rectangle:
            pos: self.pos
            size: self.size


    BoxLayout:
        id: box
        orientation: "horizontal"
        size: root.width, root.height
        padding: 50
        spacing: 50
        Image:
            id: image
            source: "" # I want to place here the image selected
            size:root.width, root.height
            pos_hint: {'x': .1, 'y': .1}


    MDScreen:
    
        MDFloatingActionButtonSpeedDial:
            callback: app.call
            
            data: 
                {'anchor': 'Original',
                'eraser': 'Noise Remove',
                'image-filter-black-white': 'Grayscale',
                'weather-sunny': 'Sépia',
                'blur': 'Blur',
                'arrow-split-horizontal': 'Motion Blur Horizontal',
                'arrow-split-vertical': 'Motion Blur Vertical',
                'shape': 'Canny',
                'contrast': 'Bri/Contr'}
            id: floatbtn
            # data: app.data
            root_button_anim: True
            hint_animation: False
            bg_hint_color: app.theme_cls.primary_dark
    
    SmoothButton:
        text: "Save"
        opacity: 0
        disabled: True
        id:save_btn
        size_hint: 0.1, 0.07
        pos_hint: {"center_x": .1, "center_y": .13}
        on_press: app.save()
        # on_release:

    SmoothButton:
        text: "Cancel"
        id:cancel_btn
        size_hint: 0.1, 0.07
        pos_hint: {"center_x": .1, "center_y": .05}
        on_release:
            app.root.current = "main"
            root.manager.transition.direction = "right"
            app.exit_manager()
            #app.file_manager_open()



    Slider:
        id: slid
        opacity: 0
        disabled: True
        size_hint: 0.5, 0.1
        value: 1
        step: 2
        min: 1
        max: 71
        on_value: 
            #label.text = str(self.value)
            app.new_valor(int(self.value))
        
        pos_hint:{'center_x': .5, 'center_y': .14}
    
    Label:
        opacity: 0
        id: label
        font_size: 12
        text: "Contrast"
        pos_hint:{'center_x': .2, 'center_y': .14}
    
    Slider:
        id: slid2
        opacity: 0
        disabled: True
        size_hint: 0.5, 0.1
        value: 0.1
        step: 2
        min: 0.1
        max: 71
        on_value: 
            #label.text = str(self.value)
            app.new_valor(int(self.value))
        
        pos_hint:{'center_x': .5, 'center_y': .05}
        
    Label:
        opacity: 0
        id: label2
        font_size: 12
        text: "Brightness"
        pos_hint:{'center_x': .2, 'center_y': .05}
        
<SmoothButton@Button>:
    size: 0.6, 0.1
    background_color: (0,0,0,0)
    background_normal: ''
    back_color: (4/255,84/255,150/255,1)
    on_press: self.back_color = (5/255,104/255,195/255,1)
    on_release: self.back_color = (4/255,84/255,150/255,1)
    canvas.before:
        Color:
            rgba: self.back_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [18]

"""
class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass



class MyMainApp(MDApp):


    def file_manager_open(self):
        self.file_manager.show("/Users/Evair/PycharmProjects/gpu/Filemanager/img")  # output manager to the screen
        self.manager_open = True


    def __init__(self, **kwargs):
        super(MyMainApp, self).__init__(**kwargs)



        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
            select_path=self.select_path,  # function called when selecting a file/directory
            #preview=True,
        )

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        """
        self.caminho = path
        filename, self.extension = os.path.splitext(self.caminho)
        self.imagem = PilImage.open(path)

        self.exit_manager()
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.root.get_screen('second').ids.image.source = path
            toast(path, duration=1.0)
        else:
            toast('Este arquivo não é uma imagem')
            self.exit_manager()
            self.file_manager_open()

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""
        if self.caminho == None:
            MDApp.get_running_app.stop()
        self.manager_open = False
        self.file_manager.close()

    def option_callback(self, text_of_option):
        print(text_of_option)

    def new_valor(self, value):
        self.valor_slide = value
        if self.valor_slide > 0:
            self.call(self.btn)


        else:
            self.call(self.btn)



    def call(self, button):

        self.btn = button

        if button.icon == "anchor":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            self.ori_converted_image = np.array(self.imagem.convert('RGB'))
            buf1 = cv2.flip(self.ori_converted_image, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(self.ori_converted_image.shape[1], self.ori_converted_image.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 0
            self.root.get_screen('second').ids.slid.disabled = True
            self.root.get_screen('second').ids.slid2.opacity = 0
            self.root.get_screen('second').ids.slid2.disabled = True


        if button.icon == "eraser":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            self.root.get_screen('second').ids.slid.max = 21
            self.root.get_screen('second').ids.slid.step = 2
            self.root.get_screen('second').ids.slid.min = 1
            self.converted_image_rem = np.array(self.imagem.convert('RGB'))
            if self.converted_image_rem.shape[0] > 2000:
                self.redu_image = cv2.imread(self.caminho, cv2.IMREAD_REDUCED_COLOR_4)
                b, g, r = cv2.split(self.redu_image)  # get b,g,r
                rgb_img = cv2.merge([r, g, b])  # switch it to rgb
                self.denoised_image = cv2.fastNlMeansDenoisingColored(rgb_img, None, self.root.get_screen('second').ids.slid.value, self.root.get_screen('second').ids.slid.value, 7, 21)
                self.larger = cv2.resize(self.denoised_image, (self.converted_image_rem.shape[1], self.converted_image_rem.shape[0]), interpolation=cv2.INTER_CUBIC)
                print(self.denoised_image.shape, self.converted_image_rem.shape)
                buf1 = cv2.flip(self.larger, 0)
                buf = buf1.tobytes()
                texture1 = Texture.create(size=(self.converted_image_rem.shape[1], self.converted_image_rem.shape[0]), colorfmt='rgb')
                texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.root.get_screen('second').ids.image.texture = texture1
                self.root.get_screen('second').ids.slid.opacity = 1
                self.root.get_screen('second').ids.slid.disabled = False
                self.root.get_screen('second').ids.slid2.opacity = 0
                self.root.get_screen('second').ids.slid2.disabled = True
            else:
                self.denoised_image = cv2.fastNlMeansDenoisingColored(self.converted_image_rem, None,
                                                                      self.root.get_screen('second').ids.slid.value,
                                                                      self.root.get_screen('second').ids.slid.value, 7, 21)

                print(self.denoised_image.shape, self.converted_image_rem.shape)
                buf1 = cv2.flip(self.denoised_image, 0)
                buf = buf1.tobytes()
                texture1 = Texture.create(size=(self.converted_image_rem.shape[1], self.converted_image_rem.shape[0]), colorfmt='rgb')
                texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.root.get_screen('second').ids.image.texture = texture1
                self.root.get_screen('second').ids.slid.opacity = 1
                self.root.get_screen('second').ids.slid.disabled = False
                self.root.get_screen('second').ids.slid2.opacity = 0
                self.root.get_screen('second').ids.slid2.disabled = True

        if button.icon == "weather-sunny":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.slid.step = 2
            self.root.get_screen('second').ids.slid.min = 1
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            converted_image = np.array(self.imagem.convert('RGB'))
            res = cv2.cvtColor(converted_image, cv2.COLOR_BGR2RGB)  # converting to RGB as sepia matrix is for RGB
            res = np.array(res, dtype=np.float32)
            res = cv2.transform(res, np.matrix([[0.393, 0.769, 0.189],
                                                [0.349, 0.686, 0.168],
                                                [0.272, 0.534, 0.131]]))
            res[np.where(res > 255)] = 255  # clipping values greater than 255 to 255
            self.res = np.array(res, dtype=np.uint8)
            #self.res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            buf1 = cv2.flip(self.res, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(res.shape[1], res.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 0
            self.root.get_screen('second').ids.slid.disabled = True
            self.root.get_screen('second').ids.slid2.opacity = 0
            self.root.get_screen('second').ids.slid2.disabled = True

        if button.icon == "image-filter-black-white":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.slid.step = 2
            self.root.get_screen('second').ids.slid.min = 1
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            converted_image = np.array(self.imagem.convert('RGB'))
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)

            img2 = np.zeros_like(converted_image)
            img2[:, :, 0] = gray_image
            img2[:, :, 1] = gray_image
            img2[:, :, 2] = gray_image
            self.gray = img2
            buf1 = cv2.flip(img2, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(gray_image.shape[1], gray_image.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 0
            self.root.get_screen('second').ids.slid.disabled = True
            self.root.get_screen('second').ids.slid2.opacity = 0
            self.root.get_screen('second').ids.slid2.disabled = True

        if button.icon == "blur":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.slid.step = 2
            self.root.get_screen('second').ids.slid.min = 1
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            self.root.get_screen('second').ids.slid.max = 71
            converted_image = np.array(self.imagem.convert('RGB'))
            redu_image = cv2.resize(converted_image, None, fx=0.9, fy=0.9, interpolation=cv2.INTER_LINEAR)
            self.blur_image = cv2.GaussianBlur(redu_image, (int(self.root.get_screen('second').ids.slid.value), int(self.root.get_screen('second').ids.slid.value)), 0, 0)
            buf1 = cv2.flip(self.blur_image, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(redu_image.shape[1], redu_image.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 1
            self.root.get_screen('second').ids.slid.disabled = False
            self.root.get_screen('second').ids.slid2.opacity = 0
            self.root.get_screen('second').ids.slid2.disabled = True

        if button.icon == "arrow-split-horizontal":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.slid.step = 2
            self.root.get_screen('second').ids.slid.min = 1
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            self.root.get_screen('second').ids.slid.max = 101
            converted_image = np.array(self.imagem.convert('RGB'))
            kernel_size = int(self.root.get_screen('second').ids.slid.value)
            # Create the vertical kernel.
            kernel_h = np.zeros((kernel_size, kernel_size))
            # Fill the middle row with ones.
            kernel_h[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
            # Normalize.
            kernel_h /= kernel_size
            # Apply the horizontal kernel.
            self.horizonal_mb = cv2.filter2D(converted_image, -1, kernel_h)
            buf1 = cv2.flip(self.horizonal_mb, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(converted_image.shape[1], converted_image.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 1
            self.root.get_screen('second').ids.slid.disabled = False
            self.root.get_screen('second').ids.slid2.opacity = 0
            self.root.get_screen('second').ids.slid2.disabled = True

        if button.icon == "arrow-split-vertical":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.slid.step = 2
            self.root.get_screen('second').ids.slid.min = 1
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            self.root.get_screen('second').ids.slid.max = 101
            converted_image = np.array(self.imagem.convert('RGB'))
            kernel_size = int(self.root.get_screen('second').ids.slid.value)
            # Create the vertical kernel.
            kernel_v = np.zeros((kernel_size, kernel_size))


            # Fill the middle row with ones.
            kernel_v[:, int((kernel_size - 1) / 2)] = np.ones(kernel_size)
            # Normalize.
            kernel_v /= kernel_size
            # Apply the vertical kernel.
            self.vertical_mb = cv2.filter2D(converted_image, -1, kernel_v)
            buf1 = cv2.flip(self.vertical_mb, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(converted_image.shape[1], converted_image.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 1
            self.root.get_screen('second').ids.slid.disabled = False
            self.root.get_screen('second').ids.slid2.opacity = 0
            self.root.get_screen('second').ids.slid2.disabled = True


        if button.icon == "shape":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.label.opacity = 0
            self.root.get_screen('second').ids.label2.opacity = 0
            converted_image = np.array(self.imagem.convert('RGB'))
            blur_image = cv2.GaussianBlur(converted_image, (7, 7), 0)
            canny = cv2.Canny(blur_image, 100, 150)
            self.canny = cv2.merge((canny, canny, canny))
            buf1 = cv2.flip(self.canny, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(blur_image.shape[1], blur_image.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 0
            self.root.get_screen('second').ids.slid.disabled = True
            self.root.get_screen('second').ids.slid2.opacity = 0
            self.root.get_screen('second').ids.slid2.disabled = True



        if button.icon == "contrast":
            self.root.get_screen('second').ids.save_btn.opacity = 1
            self.root.get_screen('second').ids.save_btn.disabled = False
            self.root.get_screen('second').ids.label.opacity = 1
            self.root.get_screen('second').ids.label2.opacity = 1
            self.root.get_screen('second').ids.slid.max = 2
            self.root.get_screen('second').ids.slid.min = 1
            self.root.get_screen('second').ids.slid2.max = 3
            self.root.get_screen('second').ids.slid2.min = 0.1

            print(self.root.get_screen('second').ids.slid2.value)
            self.root.get_screen('second').ids.slid2.step = .1
            self.root.get_screen('second').ids.slid.step = .1
            enhancer = ImageEnhance.Contrast(self.imagem.convert('RGB'))
            brit_enh = ImageEnhance.Brightness(self.imagem.convert('RGB'))
            contrast_img = enhancer.enhance(self.root.get_screen('second').ids.slid.value)
            bright = brit_enh.enhance(self.root.get_screen('second').ids.slid2.value)
            contrasted_img = np.array(contrast_img)
            brightest_img = np.array(bright)
            self.result = cv2.add(brightest_img, contrasted_img)
            buf1 = cv2.flip(self.result, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(contrasted_img.shape[1], contrasted_img.shape[0]), colorfmt='rgb')
            texture1.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.root.get_screen('second').ids.image.texture = texture1
            self.root.get_screen('second').ids.slid.opacity = 1
            self.root.get_screen('second').ids.slid.disabled = False
            self.root.get_screen('second').ids.slid2.opacity = 1
            self.root.get_screen('second').ids.slid2.disabled = False





    def save(self):
        if self.btn.icon == 'anchor':
            im = PilImage.fromarray(self.ori_converted_image)
            im.save(f"Noise_remover_original_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == 'eraser' and self.converted_image_rem.shape[0] > 2000:
            im = PilImage.fromarray(self.larger)
            im.save(f"Noise_remover_remover_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        else:
            im = PilImage.fromarray(self.denoised_image)
            im.save(f"Noise_remover_remover_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == 'weather-sunny':
            im = PilImage.fromarray(self.res)
            im.save(f"Noise_remover_sepia_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == 'image-filter-black-white':
            im = PilImage.fromarray(self.gray)
            im.save(f"Noise_remover_Gray_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == "blur":
            im = PilImage.fromarray(self.blur_image)
            im.save(f"Noise_remover_Blur_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == "arrow-split-horizontal":
            im = PilImage.fromarray(self.horizonal_mb)
            im.save(f"Noise_remover_MotionBH_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == "arrow-split-vertical":
            im = PilImage.fromarray(self.vertical_mb)
            im.save(f"Noise_remover_MotionBV_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == "shape":
            im = PilImage.fromarray(self.canny)
            im.save(f"Noise_remover_Canny_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)
        if self.btn.icon == "contrast":
            im = PilImage.fromarray(self.result)
            im.save(f"Noise_remover_B_C_{np.random.randint(1, 10000)}{self.extension.lower()}")
            toast("Saved", duration=1.1)

    def build(self):
        self.icon = 'img/icon.png'
        self.root = Builder.load_string(root_kv)

if __name__ == "__main__":
    MyMainApp(title="Noyse Remove and editing").run()