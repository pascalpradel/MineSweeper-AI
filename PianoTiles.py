import time
import pyautogui
import keyboard

class PianoTiles(object):
    def __init__(self):
        print("Init started..")
        self.tile_1 = [965,705]
        self.tile_2 = [1180,705]
        self.tile_3 = [1395,705]
        self.tile_4 = [1610,705]

        self.all_tiles = [self.tile_1, self.tile_2, self.tile_3, self.tile_4]

        self.color = [16,30,50]

        self.abweichung = [50,50,100]

        print("Init ready..")
        

    def start(self):
        print("Started..")
        time.sleep(2)
        while True:
            print("New Run")
            self.screen_read()

            if keyboard.is_pressed('esc') == True:
                    print("Bye..")
                    exit()

    def screen_read(self):
        screen = pyautogui.screenshot()

        i = 0

        while i < 4:
            tile = self.all_tiles[0] 
            pixel = screen.getpixel((tile[0],tile[1]))
            if self.check_pixel(pixel, self.color):
                pyautogui.moveTo(tile[0], tile[1])
                pyautogui.click(button='left')
            i += 1

    def check_pixel(self, pixel, color_to_find):
        if pixel[0] > color_to_find[0] - self.abweichung[0] and pixel[0] < color_to_find[0] + self.abweichung[0]:
            if pixel[1] > color_to_find[1] - self.abweichung[1] and pixel[1] < color_to_find[1] + self.abweichung[1]:
                if pixel[2] > color_to_find[2] - self.abweichung[2] and pixel[2] < color_to_find[2] + self.abweichung[2]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
        
       

if __name__ == "__main__":
    bot = PianoTiles()
    bot.start()