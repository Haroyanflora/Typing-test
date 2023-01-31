import pygame
from pygame.locals import *
import sys
import time
import random

# from time import time
import numpy as np
import matplotlib.pyplot as plt

import datetime

# 1100 x 800
#init function-ov karucvum e constructor-y yev sahmanvum en bolor variable-nery, bolorin skzbnakan pulum trvum e zroyakan arjeq
# width, height of window, images

class Game:

    def __init__(self):
        self.w = 1100
        self.h = 800
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.input_text_new = ""
        self.correct_numbers = 0
        self.incorrect_numbers = 0
        self.incorrect_letters = ""
        self.results1 = 'Incorrect letters'
        self.results2 = "Time:0 Accuracy:0 % Wpm:0 Incorrect letters:0 Correct letters:0"
        self.letter_list = []
        self.event_list = []
        self.list1 = [0]
        self.wpm = 0
        self.end = False
        #colors
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C1 = (255, 0, 0)
        self.RESULT_C2 = (255, 213, 102)
        self.RESULT_C3 = (255, 0, 0)

        pygame.init()
        self.open_img = pygame.image.load('typing-test.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))
        self.bg = pygame.image.load('b1.jpg')
        self.bg = pygame.transform.scale(self.bg, (1100, 800))
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed test')

    #draw-text function-ov texty cucadrvum e ekranin, trvum e parametrery
    def draw_text(self, screen, msg, y, fsize, color): #msg = "Typing Speed Test"
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

#    random sentence naxadasutyuny sentences.txt file-ic yntrvum e random kargov
    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

     # calculatuin of typing time, WPM, Accuracy, bolor hashvarknery katarvum en, stexcvum e result masy,
    # vortex nerarvac en bolor variable-nery voronq petq e artacolven ekranin
    def show_results(self, screen):
        if (not self.end):
            # Calculate time
            self.total_time = time.time() - self.time_start
            # Calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
            print(self.total_time)
            # Calculate accuracy
            count = 0
            incorrect_letters = ""
            correct_let = []
            input_text_new = ""
            for i, c in enumerate(self.input_text):  #i-index, c - andam
                try:
                    if self.word[i] != c:
                        count += 1
                        incorrect_letters += self.input_text[i]
                        input_text_new += self.input_text[i]
                    else:
                        correct_let.append(self.input_text[i])
                        input_text_new += self.input_text[i]
                except:
                    count += 1
            try:
                self.accuracy = (len(self.input_text) - count) / len(self.input_text) * 100
            except:
                self.accuracy = 0
            self.correct_numbers = len(self.input_text) - count
            self.incorrect_numbers = count
            self.incorrect_letters = incorrect_letters
            self.input_text_new = input_text_new

            self.results1 = '  Incorrect letters: ' + self.incorrect_letters
            self.results2 = '  Time:' + str(round(self.total_time)) + " secs   Accuracy:" + str(
                round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm)) + "   Incorrect letters: " +\
                            str(self.incorrect_numbers)  + "   Correct letters:  " + str(self.correct_numbers)
            self.results3 = self.input_text_new
            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            # screen.blit(self.time_img, (80,320)) reset grvacqi u icon nkari texadrvacutyunn e
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))
            print(self.results1)
            print(self.results2)
            print(self.results3)
            pygame.display.update()

    #amenakarevor function-n e, vory bolory eventnery fixum e /mkniki click, enter kochaki sexmum/ skzbum rest anelov bolor argument-nery
    def run(self):
        self.reset_game()

        self.running = True
        while (self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (200, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (200, 250, 650, 50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    print(x, y)  #x,y kordinatnern en te voret e gtnvum mkniky
                    # position of input box, clicking input box to start typing
                    if (x >= 50 and x <= 650 and y >= 250 and y <= 300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                        # position of reset box, clicking reset box to reset the game
                    if (x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()


                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key != pygame.K_RETURN:
                            self.event_list.append(time.time() - self.time_start)
                            print(time.time(), self.time_start)
                            # list_new = self.event_list
                            print("event_list", self.event_list)
                            self.list1 = [0]
                            for i in range(len(self.event_list) - 2):
                                self.list1.append(self.event_list[i+2] - self.event_list[i+1])
                        print("list1", self.list1)
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results1)
                            print(self.results2)
                            self.draw_text(self.screen, self.results1, 400, 28, self.RESULT_C1)
                            self.draw_text(self.screen, self.results2, 350, 28, self.RESULT_C2)
                            # self.draw_text(self.screen, self.results3, 450, 28, self.RESULT_C2)
                            self.end = True
                            #graph, vorin vorpes input arjeq trvum e list, vory cuyc e talis amen type arac character-i jamanaky
                            x = np.array(self.list1)
                            y = np.array(range(1, len(self.list1) + 1))
                            print(x)
                            print(y)
                            font1 = {'color': 'blue', 'size': 20}
                            font2 = {'color': 'darkred', 'size': 15}
                            plt.plot(y, x, marker="o", linestyle='dotted')
                            plt.title("Seconds per character", fontdict=font1)
                            plt.xlabel("Typed characters", fontdict=font2)
                            plt.ylabel("Letters per second", fontdict=font2)
                            time.sleep(2)
                            plt.show()

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()
        clock.tick(60)
    #bolor variable-nery krkin zroyacvum en
    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.event_list = []
        # Get random sentence
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        # drawing heading
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (200, 250, 650, 50), 2)
        # draw the sentence string
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)
        pygame.display.update()


Game().run()
