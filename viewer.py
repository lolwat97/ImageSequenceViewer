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

        # сохраняем пути картинок всех
        self.imageFilenames = [os.path.join(self.path, file) for file in os.listdir(self.path)]

        # грузим картинки в Label-объекты, привязанные к фрейму для тамбнейликов
        self.imageThumbnailLabels = self.makeImageLabels(self.imageThumbnailFrame, self.imageFilenames, self.thumbSize)

        self.setImagePreviewLabel(self.imagePreviewFrame, self.imageFilenames[0], self.previewSize)

        self.previewLabel.pack() # запихиваем превьюшку в imagePreview
        self.packFrames() # запихиваем фреймы в главное окно
        self.packImages(self.imageThumbnailLabels) # запихиваем тамбнейлики в imageGrid

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
            label.image = photoimage # wtf
            # >You must keep a reference to the image object in your Python program, either by storing it in a global
            # >variable, or by attaching it to another object.
            # глупо сделали, ака "делай так и будет работать"
            imageLabels.append(label) # запихиваем получившийся лейбл в imageLabels
        return imageLabels # который и возвращаем

    def packImages(self, imageLabels):
        for label in imageLabels:
            label.pack() # запихиваеееем

    def run(self):
        self.root.mainloop() # пошло выполнение программы