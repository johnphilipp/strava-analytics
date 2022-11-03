class Collage():
    def __init__(self, images, len, heigth, width):
        self._images = images
        self._len = len
        self._height = heigth
        self._width = width


    def get_collage(self):
        """
        Return a collage with cropped images of polylines
        """
        imgs = []
        for i in range(0, self._len):
            imgs.append()

        collage = Image.new("RGBA",
                            (self._width, self._height),
                            color=(255, 255, 255, 255))
        c = 0
        for i in range(0, specs["h"], specs["wh_single"]):
            for j in range(0, specs["w"], specs["wh_single"]):
                if c < len(imgs):
                    photo = imgs[c].convert("RGBA")
                    photo = photo.resize(
                        (specs["wh_single"], specs["wh_single"]))

                    collage.paste(photo, (j, i))
                    c += 1
        return collage
    


def main():
    import json

    with open('data/activities_public.json') as f:
        json_data = json.load(f)

    new_poster = Collage()


if __name__ == "__main__":
    main()
