import time
import pyautogui
import keyboard
import cv2
import numpy as np

class MineSweeperBot(object):
    def __init__(self):
        print("Init started..")

        ############SETTINGS############
        self.count_rows = 16
        self.count_lines = 16

        self.start_point = [580,135]

        self.box_size = [63,62]

        self.abstand_x = 4
        self.abstand_y = 5
        ################################

        self.board = [[0 for x in range(self.count_rows)] for y in range(self.count_lines)] 
        self.prob_board = [[0 for x in range(self.count_rows)] for y in range(self.count_lines)] 

        self.color_blue = [124,210,255]
        self.color_board = [255,255,255]

        #self.color_flag = [230,210,65]
        #self.color_flag_2 = [230,160,50]
        #self.color_one = [25,289,224]
        #self.color_one_2 = [50,190,218]
        #self.color_two = [134,165,60]
        #self.color_three = [216,26,101]

        self.abweichung = [25,25,25] #in Pixeln

        self.rounds_since_last_klick = 0

        self.size_scale = 2
        print("Init ready..")
        

    def start(self):
        

        time.sleep(2)
        print("Started..")

        self.leftclick(int(self.start_point[0]+self.box_size[0]/2),int(self.start_point[1]+self.box_size[1]/2))

        self.fill()
        while True:
            if keyboard.is_pressed('esc') == True:
                    print("Bye..")
                    exit()

            self.screen_read()
            self.fill_probability(self.prob_board)
            image1 = self.target_boxes(1)
            
            self.rule_clear_field()
            self.execute_order()

            time.sleep(1)  

            image2 = self.target_boxes(2)
            self.show_image(image1, image2)

            #print(self.board)
            #print(self.prob_board)     
            
            """
            while True:
                if keyboard.is_pressed('ctrl') == True:
                    time.sleep(0.5)
                    break
            #"""
            
            

    def fill_probability(self, prob_board):
        self.fill_board(prob_board)

        i = 0
        j = 0
        
        while i < self.count_rows:
            while j < self.count_lines:
                percentage = 0
                box = self.board[i][j]

                x = i
                y = j
                item_id = box[2]
                
                if item_id >= 2:
                    if item_id == 3:
                        percentage = 100
                    elif item_id == 4:
                        percentage = 200
                    elif item_id == 5:
                        percentage = 300
                    elif item_id == 6:
                        percentage = 400
                    #USW

                    box_field = [[0 for x in range(3)] for y in range(3)]
                    
                    counter_x = -1
                    counter_y = -1

                    blue_counter = 0
                    flag_counter = 0

                    while counter_x < 2:
                        while counter_y < 2:
                            if x+counter_x >= 0 and y+counter_y >= 0 and x+counter_x < self.count_rows and y+counter_y < self.count_lines:
                                box_data = self.board[x+counter_x][y+counter_y]
                                field_input = [x+counter_x, y+counter_y, box_data[2]]
                                box_field[counter_x+1][counter_y+1] = field_input
                                if box_data[2] == 0:
                                    blue_counter += 1
                                elif box_data[2] == 2:
                                    flag_counter += 1
                            else:
                                box_field[counter_x+1][counter_y+1] = [404,404,404]

                            counter_y += 1
                        counter_y = -1
                        counter_x += 1

                    if blue_counter > 0:
                        a_iterator = 0
                        b_iteraror = 0

                        temp_percentage = percentage - (flag_counter * 100)

                        while a_iterator < 3:
                            while b_iteraror < 3:
                                box_field_data = box_field[a_iterator][b_iteraror]
                                if box_field_data[2] == 0:
                                    prob_board_data = prob_board[box_field_data[0]][box_field_data[1]]
                                    if percentage != 0:
                                        prob_board_data[0] = prob_board_data[0]+int(temp_percentage/blue_counter)
                                    prob_board_data[1] += 1
                                    prob_board[box_field_data[0]][box_field_data[1]] = prob_board_data
                                b_iteraror += 1
                            a_iterator += 1
                            b_iteraror = 0
                    
                    #print("X: " + str(x) + " " + "Y: " + str(y))
                    #print(box)
                    #print(box_field)

                j += 1
            i += 1
            j = 0
        
        return prob_board


    def fill(self):
        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                x = int((self.start_point[0]) + (self.box_size[0]/2) + (i*self.box_size[0]) + (i*self.abstand_x))
                y = int((self.start_point[1]) + (self.box_size[1]/2) + (j*self.box_size[1]) + (j*self.abstand_y))

                input_data = [x,y,0]
                self.board[j][i] = input_data

                j += 1
            i += 1
            j = 0


    def fill_board(self, board):
        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                board[j][i] = [0,0]
                j += 1
            i += 1
            j = 0

    
    def screen_read(self):
        error_counter = 0

        screen = pyautogui.screenshot()
        i = 0
        j = 0
        
        while i < self.count_rows:
            while j < self.count_lines:
                box = self.board[j][i]
                pixel = screen.getpixel((box[0],box[1]))

                x_pixel = int(box[0] - int(self.box_size[0]/2))
                y_pixel = int(box[1] - int(self.box_size[1]/2))

                if pyautogui.locateOnScreen('one_16x16.PNG', region=(x_pixel,y_pixel, self.box_size[0], self.box_size[1]), grayscale=True, confidence=0.9) != None:
                    box_id = 3 #"ONE"
                elif self.check_pixel(pixel, self.color_blue, self.abweichung):
                    box_id = 0 #"BLAU"
                elif pyautogui.locateOnScreen('white_16x16.PNG', region=(x_pixel,y_pixel, self.box_size[0], self.box_size[1]), grayscale=False, confidence=0.9) != None:
                    box_id = 1 #"WEIß" 
                elif pyautogui.locateOnScreen('flag_16x16.PNG', region=(x_pixel,y_pixel, self.box_size[0], self.box_size[1]), grayscale=True, confidence=0.9) != None:
                    box_id = 2 #"FLAG"
                elif pyautogui.locateOnScreen('two_16x16.PNG', region=(x_pixel,y_pixel, self.box_size[0], self.box_size[1]), grayscale=True, confidence=0.9) != None:
                    box_id = 4 #"TWO"
                elif pyautogui.locateOnScreen('three_16x16.PNG', region=(x_pixel,y_pixel, self.box_size[0], self.box_size[1]), grayscale=True, confidence=0.9) != None:
                    box_id = 5 #"THREE"
                elif pyautogui.locateOnScreen('four_16x16.PNG', region=(x_pixel,y_pixel, self.box_size[0], self.box_size[1]), grayscale=True, confidence=0.9) != None:
                    box_id = 6 #"FOUR"
                else:
                    print("Error: Color/Picture not found at: " + str(i+1) + "/" + str(j+1))
                    error_counter += 1
                    if error_counter >= 5:
                        exit()
                    box_id = 404

                box[2] = box_id
                self.board[j][i] = box

                j += 1
            i += 1
            j = 0


    def check_pixel(self, pixel, color_to_find, abweichung):
        if pixel[0] > color_to_find[0] - abweichung[0] and pixel[0] < color_to_find[0] + abweichung[0]:
            if pixel[1] > color_to_find[1] - abweichung[1] and pixel[1] < color_to_find[1] + abweichung[1]:
                if pixel[2] > color_to_find[2] - abweichung[2] and pixel[2] < color_to_find[2] + abweichung[2]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    def execute_order(self):
        highest_number = [0,0,0,0] #x,y,perc,menge an bestätigungen
        lowest_number = [0,0,1000,0]

        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                prob_board_data = self.prob_board[j][i]
                
                if prob_board_data[1] != 0:
                    if highest_number[2] <= prob_board_data[0] and highest_number[3] <= prob_board_data[1]:
                        highest_number = [j,i,prob_board_data[0],prob_board_data[1]]
                        
                    if lowest_number[2] >= prob_board_data[0] and lowest_number[3] <= prob_board_data[1]:
                            lowest_number = [j,i,prob_board_data[0],prob_board_data[1]]
                j += 1
            i += 1
            j = 0


        if lowest_number[3] > 9:
            data = self.board[lowest_number[0]][lowest_number[1]]
            print("Left-Klick: " + str(lowest_number[0]) + " /" +  str(lowest_number[1]))
            self.leftclick(data[0],data[1])
        elif highest_number[2] > 999:
            data = self.board[highest_number[0]][highest_number[1]]
            print("Right-Klick: " + str(highest_number[0]) + " /" +  str(highest_number[1]))
            self.rightclick(data[0],data[1])
        elif self.blick_in_die_zukunft(highest_number[0],highest_number[1]) == False:
            data = self.board[highest_number[0]][highest_number[1]]
            print("Right-Klick: " + str(highest_number[0]) + " /" +  str(highest_number[1]))
            self.rightclick(data[0],data[1])
        else:
            data = self.board[lowest_number[0]][lowest_number[1]]
            print("Left-Klick: " + str(lowest_number[0]) + " /" +  str(lowest_number[1]))
            self.leftclick(data[0],data[1])

        #print(lowest_number)
        #print(highest_number)
        #exit()


    def leftclick(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click(button='left')
        pyautogui.moveTo(self.start_point[0], self.start_point[1])

    def rightclick(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click(button='right')
        pyautogui.moveTo(self.start_point[0], self.start_point[1])

    
    def target_boxes(self, id):
        label = ""

        screenshot = np.array(pyautogui.screenshot())

        i = 0
        j = 0

        while i < self.count_rows:
            while j < self.count_lines:
                prob_board_data = self.prob_board[j][i]
                board_data = self.board[j][i]

                if id == 1:
                    label = str(board_data[2])
                elif id == 2:
                    label = str(prob_board_data[0])

                x = board_data[0]-int(self.box_size[0]*(1/3))
                cv2.putText(screenshot,label,(x,board_data[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(50,50,50),2)

                j += 1
            i += 1
            j = 0
        
        x_end = int(self.start_point[0] + (self.count_rows*self.box_size[0]) + (self.count_rows*self.abstand_x))
        y_end = int(self.start_point[1] + (self.count_lines*self.box_size[1]) + (self.count_lines*self.abstand_y))

        screenshot = screenshot[self.start_point[1]:y_end, self.start_point[0]:x_end]
        screenshot = cv2.resize(screenshot, (screenshot.shape[1] // self.size_scale, screenshot.shape[0] // self.size_scale))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

        return screenshot
        
    def show_image(self, image1, image2):
        screenshot = np.array(pyautogui.screenshot())

        y_end = int(self.start_point[1] + (self.count_lines*self.box_size[1]) + (self.count_lines*self.abstand_y))
        screenshot = screenshot[self.start_point[1]:y_end, self.start_point[0]-50:self.start_point[0]-25]

        screenshot = cv2.resize(screenshot, (screenshot.shape[1] // self.size_scale, screenshot.shape[0] // self.size_scale))

        screenshot_comb = np.concatenate((image1, screenshot), axis=1)
        screenshot_comb = np.concatenate((screenshot_comb, image2), axis=1)
        cv2.imshow("screenshot", screenshot_comb)
        cv2.waitKey(1)

    def blick_in_die_zukunft(self,x_cord,y_cord):
        temp_board = self.board
        temp_board_data = self.board[y_cord][x_cord]
        temp_board_data[2] = 2
        temp_board[y_cord][x_cord] = temp_board_data
        
        temp_prob_board = [[0 for x in range(self.count_rows)] for y in range(self.count_lines)] 
        temp_prob_board = self.fill_probability(temp_prob_board)

        i = 0
        j = 0

        return_value = False

        while i < self.count_rows:
            while j < self.count_lines:
                prob_data = temp_prob_board[j][i]
                if prob_data[0] < 0:
                    return_value = True

                j += 1
            i += 1
            j = 0

        return return_value

    def rule_clear_field(self):
        return_value = False

        i = 0
        j = 0
        
        while i < self.count_rows:
            while j < self.count_lines:
                box = self.board[i][j]

                x = i
                y = j
                item_id = box[2]
                

                if item_id >= 2:
                    if item_id == 3:
                        flag_count = 1
                    elif item_id == 4:
                        flag_count = 2
                    elif item_id == 5:
                        flag_count = 3
                    elif item_id == 6:
                        flag_count = 4
                    #USW
                
                box_field = [[0 for x in range(3)] for y in range(3)]

                counter_x = -1
                counter_y = -1

                flag_counter = 0
                blue_counter = 0


                if box[2] != 0 and box[2] != 1 and box[2] != 2:
                    while counter_x < 2:
                        while counter_y < 2:
                            if x+counter_x >= 0 and y+counter_y >= 0 and x+counter_x < self.count_rows and y+counter_y < self.count_lines:
                                box_data = self.board[x+counter_x][y+counter_y]
                                field_input = [x+counter_x, y+counter_y, box_data[2]]
                                box_field[counter_x+1][counter_y+1] = field_input
                                if box_data[2] == 0:
                                        blue_counter += 1
                                elif box_data[2] == 2:
                                    flag_counter += 1
                            else:
                                box_field[counter_x+1][counter_y+1] = [404,404,404]

                            counter_y += 1
                        counter_y = -1
                        counter_x += 1

                    if flag_counter > 0:
                        if flag_counter == flag_count:
                            a_iterator = 0
                            b_iteraror = 0

                            while a_iterator < 3:
                                while b_iteraror < 3:
                                    box_field_data = box_field[a_iterator][b_iteraror]

                                    if box_field_data[2] == 0:
                                        prob_board_data = self.prob_board[box_field_data[0]][box_field_data[1]]
                                        prob_board_data[0] = 0
                                        prob_board_data[1] += 10
                                        self.prob_board[box_field_data[0]][box_field_data[1]] = prob_board_data

                                        return_value = True
                                    b_iteraror += 1
                                a_iterator += 1
                                b_iteraror = 0 

                        elif flag_count - flag_counter == blue_counter:
                            a_iterator = 0
                            b_iteraror = 0

                            while a_iterator < 3:
                                while b_iteraror < 3:
                                    box_field_data = box_field[a_iterator][b_iteraror]

                                    if box_field_data[2] == 0:
                                        prob_board_data = self.prob_board[box_field_data[0]][box_field_data[1]]
                                        prob_board_data[0] += 1000
                                        prob_board_data[1] += 10
                                        self.prob_board[box_field_data[0]][box_field_data[1]] = prob_board_data

                                        return_value = True
                                    b_iteraror += 1
                                a_iterator += 1
                                b_iteraror = 0 

                        elif flag_count == blue_counter:
                            a_iterator = 0
                            b_iteraror = 0

                            while a_iterator < 3:
                                while b_iteraror < 3:
                                    box_field_data = box_field[a_iterator][b_iteraror]

                                    if box_field_data[2] == 0:
                                        prob_board_data = self.prob_board[box_field_data[0]][box_field_data[1]]
                                        prob_board_data[0] += 0
                                        prob_board_data[1] += 10
                                        self.prob_board[box_field_data[0]][box_field_data[1]] = prob_board_data

                                        return_value = True
                                    b_iteraror += 1
                                a_iterator += 1
                                b_iteraror = 0 

                j += 1
            i += 1
            j = 0
        
        return return_value
        
       

if __name__ == "__main__":
    bot = MineSweeperBot()
    bot.start()