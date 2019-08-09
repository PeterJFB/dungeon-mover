
from PIL import Image

def heatMap(hist):
    print(len(hist))
    min_x, min_y = min(hist, key=lambda x: x[0])[0], min(hist, key=lambda y: y[1])[1]
    map = Image.new("RGBA", (max(hist, key=lambda x: x[0] - min_x)[0], max(hist, key=lambda y: y[1] - min_y)[1]), "black")
    map_pix = map.load()
    mul = 10
    for i, pos in enumerate(hist):
        x, y = pos[0], pos[1]
        map_pix[x - min_x, y - min_y] = (i * mul if i * mul <= 255 else 255,
                                         i * mul - 255 if i * mul - 255 <= 255 else 255,
                                         i * mul - 255 * 2 if i * mul - 255 * 2 <= 255 else 255)
    map = map.resize((100 * map.size[0], 100 * map.size[1]), Image.NEAREST)
    map.show()




        
        