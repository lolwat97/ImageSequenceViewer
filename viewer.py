from tkinter import *
from PIL import Image, ImageTk
import os
import pickle


class Viewer:
    def __init__(self):
        self.path = 'img'
        self.thumbSize = (200, 200)  # максимальный размер тамбнейликов
        self.previewSize = (500, 500)  # максимальный размер превьюшечки
        self.root = Tk()  # создаем главное окно
        self.imageThumbnailFrame = Frame(self.root)  # фрейм для тамбнейликов
        self.imagePreviewFrame = Frame(self.root)  # фрейм для превьюшки
        self.previewLabel = Label(self.imagePreviewFrame)
        self.prevClick = ''
        self.nowClick = ''
        # сохраняем пути картинок всех
        self.imageFilenames = [os.path.join(self.path, file) for file in os.listdir(self.path)]
        # грузим картинки в Label-объекты, привязанные к фрейму для тамбнейликов

        self.imageBasenames = pickle.load(open("order.pic", "rb"))

        if self.imageFilenames == self.imageBasenames:
            print("Nothing new")
            self.imageFilenames = self.imageBasenames
        else:
            print("New or deleted images")
            # if new найти и добавить новое изображение в конец бд
            for simage in self.imageFilenames:
                if simage in self.imageBasenames:
                    pass
                else:
                    print("New one: ", simage)
                    self.imageBasenames.append(simage)
            # if deleted удалить из бд, удаленное
            for bimage in self.imageBasenames:
                if bimage in self.imageFilenames:
                    pass
                else:
                    print("Deleted one: ", bimage)
                    self.imageBasenames.remove(bimage)
            self.imageFilenames = self.imageBasenames
        # pickle.dump(self.imageFilenames, open("order.pic","wb"))

        self.imageThumbnailLabels = self.make_image_labels(self.imageThumbnailFrame, self.imageFilenames,
                                                           self.thumbSize)

        self.set_image_preview_label(self.imagePreviewFrame, self.imageFilenames[0], self.previewSize)

        self.previewLabel.pack()  # запихиваем превьюшку в imagePreview
        self.previewLabel.name = "preview"
        self.previewLabel.bind("<1>", self.on_main_click)
        self.pack_frames()  # запихиваем фреймы в главное окно
        self.pack_images(self.imageThumbnailLabels)  # запихиваем тамбнейлики в imageGrid

    def set_image_preview_label(self, window, file, size):  # ставим картинку в Label для превью
        image = Image.open(file)  # открываем картинку с помощью PIL
        image.thumbnail(size, Image.ANTIALIAS)  # Уменьшаем ее до размера size
        photoimage = ImageTk.PhotoImage(image)  # Конвертируем картинку в формат TkInter
        self.previewLabel = Label(window, image=photoimage)  # Делаем Label
        self.previewLabel.image = photoimage  # Сохраняем референс (вот это глупо сделано, как по-моему, но так надо)

    def pack_frames(self):
        self.imageThumbnailFrame.pack(side='left')  # зафигачиваем тамбнейлы слева
        self.imagePreviewFrame.pack(side='right')  # а превью справа

    def make_image_labels(self, window, image_files, size):
        image_labels = []
        for file in image_files:  # для каждого файла в списке файлов
            image = Image.open(file)  # открываем с помощью PIL
            image.thumbnail(size, Image.ANTIALIAS)  # уменьшаем
            photoimage = ImageTk.PhotoImage(image)  # конвертируем в формат TkInter
            label = Label(window, image=photoimage)  # Делаем, собственно, лейбл
            label.image = photoimage  #
            # >You must keep a reference to the image object in your Python program, either by storing it in a global
            # >variable, or by attaching it to another object.
            # глупо сделали, ака "делай так и будет работать"
            image_labels.append(label)  # запихиваем получившийся лейбл в image_labels
        return image_labels  # который и возвращаем

    def pack_images(self, image_labels):
        i = 0

        for label in image_labels:
            label.pack()  # запихиваеееем
            label.path = self.imageFilenames[i]
            i += 1
            label.bind("<1>", self.on_main_click)

    def on_main_click(self, event):
        self.previewLabel.pack_forget()
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
                for label in self.imageThumbnailLabels:
                    label.pack_forget()
                self.imageThumbnailLabels = self.make_image_labels(self.imageThumbnailFrame, self.imageFilenames,
                                                                   self.thumbSize)
                for label in self.imageThumbnailLabels:
                    label.pack()  # запихиваеееем

                self.pack_images(self.imageThumbnailLabels)
                pickle.dump(self.imageFilenames, open("order.pic", "wb"))

            except ValueError:
                pass
        self.set_image_preview_label(self.imagePreviewFrame, self.nowClick, self.previewSize)
        self.previewLabel.pack()
        self.previewLabel.bind("<1>", self.on_main_click)

    def unpack_thumbnails(self):
        for label in self.imageThumbnailLabels:
            label.pack_forget()

    def on_closing(self):
        pass

    def run(self):

        self.root.mainloop()  # пошло выполнение программы
