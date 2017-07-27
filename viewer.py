from tkinter import *
from PIL import Image, ImageTk
import os

class Viewer:
    def __init__(self):
        self.path = 'img'
        self.thumbSize = (200, 200) # максимальный размер тамбнейликов
        self.previewSize = (500,500) # максимальный размер превьюшечки

        self.root = Tk() # создаем главное окно
        self.imageThumbnailFrame = Frame(self.root) # фрейм для тамбнейликов
        self.imagePreviewFrame = Frame(self.root) # фрейм для превьюшки
        self.previewLabel = Label(self.imagePreviewFrame)
        self.prevClick = ''
        self.nowClick = ''

        # сохраняем пути картинок всех
        self.imageFilenames = [os.path.join(self.path, file) for file in os.listdir(self.path)]

        # грузим картинки в Label-объекты, привязанные к фрейму для тамбнейликов
        self.imageThumbnailLabels = self.makeImageLabels(self.imageThumbnailFrame, self.imageFilenames, self.thumbSize)

        self.setImagePreviewLabel(self.imagePreviewFrame, self.imageFilenames[0], self.previewSize)

        self.previewLabel.pack() # запихиваем превьюшку в imagePreview
        self.previewLabel.name = "preview"
        self.previewLabel.bind("<1>", self.on_main_click)
        self.packFrames() # запихиваем фреймы в главное окно
        self.packImages(self.imageThumbnailLabels) # запихиваем тамбнейлики в imageGrid
        self.labels = []
        
    def setImagePreviewLabel(self, window, file, size): # ставим картинку в Label для превью
        image = Image.open(file) # открываем картинку с помощью PIL
        image.thumbnail(size, Image.ANTIALIAS) # Уменьшаем ее до размера size
        photoimage = ImageTk.PhotoImage(image) # Конвертируем картинку в формат TkInter
        self.previewLabel = Label(window, image=photoimage) # Делаем Label
        self.previewLabel.image = photoimage # Сохраняем референс (вот это глупо сделано, как по-моему, но так надо)

    def packFrames(self):
        self.imageThumbnailFrame.pack(side='left') # зафигачиваем тамбнейлы слева
        self.imagePreviewFrame.pack(side='right') # а превью справа

    def makeImageLabels(self, window, imageFiles, size):
        imageLabels = []
        for file in imageFiles: # для каждого файла в списке файлов
            image = Image.open(file) # открываем с помощью PIL
            image.thumbnail(size, Image.ANTIALIAS) # уменьшаем
            photoimage = ImageTk.PhotoImage(image) # конвертируем в формат TkInter
            label = Label(window, image=photoimage) # Делаем, собственно, лейбл
            label.image = photoimage #
            # >You must keep a reference to the image object in your Python program, either by storing it in a global
            # >variable, or by attaching it to another object.
            # глупо сделали, ака "делай так и будет работать"
            imageLabels.append(label) # запихиваем получившийся лейбл в imageLabels
        return imageLabels # который и возвращаем

    def packImages(self, imageLabels):
        i = 0
        self.labels = imageLabels
        for label in imageLabels:
            label.pack() # запихиваеееем
            label.path = self.imageFilenames[i]
            i = i+1
            label.bind("<1>", self.on_main_click)
        i = 0
        
    def on_main_click(self, event):
        try:
            print(event.widget.path)
            self.prevClick = self.nowClick
            self.nowClick = event.widget.path
        except AttributeError:
            print('swap', self.prevClick, self.nowClick)
            try:
                a = self.imageFilenames.index(self.prevClick)
                b = self.imageFilenames.index(self.nowClick)
                self.imageFilenames[a], self.imageFilenames[b] = self.imageFilenames[b], self.imageFilenames[a]
                print('new imagelist:')
                for text in self.imageFilenames:
                    print(text)
                
                
            except ValueError:
                pass

        
    def run(self):
        self.root.mainloop() # пошло выполнение программы

