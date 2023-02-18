from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import keyboard as kb
import random
import cv2

from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
from tf_agents.specs import array_spec

width = 64 #Width of the vision cone
height = 32 #Height of the vision cone
vision_angle = 90 #This says the FOV is 60 degrees
total_width = 360 / vision_angle * width
discount = 0.95
max_moves = 200
draw_foliage = True
num_foliage = 8

#This class holds all the information of the player, as well as all the objects in the environment
#This class has the mathematical functions for determining the angle and distance of objects from the player

class HuntingEnvironment(py_environment.PyEnvironment):

    def __init__(self, drawEnv = False):

        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=4, name='action')

        self._observation_spec = array_spec.BoundedArraySpec(shape=(width * height + max_moves, ), dtype=np.float32, minimum=0.0, maximum=1.0, name='observation')

        self.drawEnv = drawEnv
        self._state = self.convert_image(self.reset_env()) + self.return_memory()
        self._episode_ended = False
        self.discount = discount

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = self.convert_image(self.reset_env()) + self.return_memory()
        self._episode_ended = False
        return ts.restart(np.array(self._state, dtype = np.float32))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        if action >= 0 and action <= 3:
            self._state, reward, self._episode_ended = self.run_frame(action)
            self._state = self.convert_image(self._state) + self.return_memory()
        else:
            print(action)
            raise ValueError('`action` should be between 0 and 3 inclusive')

        if self._episode_ended:
            return ts.termination(np.array(self._state, dtype = np.float32), reward)
        else:
            return ts.transition(np.array(self._state, dtype = np.float32), reward, discount = self.discount)

    def calculate_distance(self, object):
        location = object.return_location()
        return ((self.player_location[0] - location[0]) ** 2 + (self.player_location[1] - location[1]) ** 2) ** 0.5

    def calculate_angle(self, object):
        total_distance = max(self.calculate_distance(object), 0.00001)
        location = object.return_location()
        x_diff = location[0] - self.player_location[0]
        y_diff = location[1] - self.player_location[1]

        if x_diff > 0 and y_diff > 0:
            angle = np.arccos(x_diff / total_distance)
        elif x_diff < 0 and y_diff < 0:
            angle = (np.arccos(abs(x_diff / total_distance)) + np.pi)
        elif x_diff < 0:
            angle = np.arccos(x_diff / total_distance)
        elif y_diff < 0:
            angle = np.arcsin(y_diff / total_distance)
        elif x_diff >= 0.0:
            angle = np.arcsin(y_diff / total_distance)
        if angle > np.pi:
            angle -= np.pi * 2
        return angle * (180 / np.pi)

    def return_looking_angle(self):
        return self.player_rotation

    def move_player(self, distance):
        angle = self.player_rotation * (np.pi / 180)
        self.player_location = [self.player_location[0] + (distance * np.cos(angle)), self.player_location[1] + (distance * np.sin(angle))]

        if self.player_location[0] < -10.0:
            self.player_location[0] = -10.0
        elif self.player_location[0] > 10.0:
            self.player_location[0] = 10.0
        if self.player_location[1] < -10.0:
            self.player_location[1] = -10.0
        elif self.player_location[1] > 10.0:
            self.player_location[1] = 10.0

    def turn_player(self, amount):
        self.player_rotation += amount
        if self.player_rotation >= 180.0:
            self.player_rotation -= 360.0
        elif self.player_rotation < -180.0:
            self.player_rotation += 360.0
    
    def add_object(self, object):
        self.objects.append(object)

    def return_objects(self):
        return self.objects.copy()

    def reset_env(self):
        self.player_location = [0,0]
        self.player_rotation = 0.0
        self.score = 0.0
        self.num_moves = 0
        self.objects = []
        self.memory = []
        if draw_foliage:
            for i in range(num_foliage):            
                self.objects.append(Object([np.cos(i / num_foliage * 2 * np.pi) * 5, np.sin(i / num_foliage * 2 * np.pi) * 5], 16, [47, 74, 44]))
                self.objects.append(Object([np.cos(i / num_foliage * 2 * np.pi) * 10, np.sin(i / num_foliage * 2 * np.pi) * 10], 16, [47, 74, 44]))

        prey_x = random.randint(-5, 5)
        prey_y = random.randint(-5, 5)
        if prey_x >= 0:
            prey_x += 5
        else:
            prey_x -= 5
        if prey_y >= 0:
            prey_y += 5
        else:
            prey_y -= 5
        self.objects.append(Object([prey_x, prey_y], 8, [255, 255, 255]))
        self.prev_distance = self.calculate_prey_distance()
        self.score -= self.prev_distance

        cv2.destroyAllWindows()
        if self.drawEnv:
            img = np.zeros((height, width, 3), dtype=np.uint8)
            img = self.draw_objects(self.sort_objects(self.return_objects()), img)
            img = cv2.resize(img, (1024, 512))
            cv2.imshow('Environment', img)
            cv2.waitKey(100)

        return self.generate_image(self.return_objects())

    def move_prey(self):
        self.objects[-1].location[0] += (random.randint(-500, 500) / 1000)
        self.objects[-1].location[1] += (random.randint(-500, 500) / 1000)
        if self.objects[-1].location[0] < -10.0:
            self.objects[-1].location[0] = -10.0
        elif self.objects[-1].location[0] > 10.0:
            self.objects[-1].location[0] = 10.0
        if self.objects[-1].location[1] < -10.0:
            self.objects[-1].location[1] = -10.0
        elif self.objects[-1].location[1] > 10.0:
            self.objects[-1].location[1] = 10.0

    def calculate_prey_distance(self):
        distance_from_prey = self.calculate_distance(self.objects[-1])
        return distance_from_prey

    def run_frame(self, action):
        reward = 0
        if action == 0:
            self.move_player(1)
        elif action == 1:
            self.move_player(-1)
        elif action == 2:
            self.turn_player(-15)
        elif action == 3:
            self.turn_player(15)
        elif action == 4:
            #do nothing
            pass

        self.memory.append(action)

        if self.drawEnv:
            img = np.zeros((height, width, 3), dtype=np.uint8)
            img = self.draw_objects(self.sort_objects(self.return_objects()), img)
            img = cv2.resize(img, (1024, 512))
            cv2.imshow('Environment', img)
            cv2.waitKey(100)
        
        prey_distance = self.calculate_prey_distance()
        self.score += 5 * (self.prev_distance - prey_distance) - (100 / max_moves)
        reward += 5 * (self.prev_distance - prey_distance) - (100 / max_moves)
        self.num_moves += 1
        prey_angle = self.return_looking_angle() - self.calculate_angle(self.objects[-1])
        if prey_distance < 2 and prey_angle <= 45 and prey_angle >= -45:
            self.score += prey_distance + 100
            reward += prey_distance + 100
            #print("caught prey")
            return self.generate_image(self.return_objects()), reward, True
        elif self.num_moves >= max_moves:
            return self.generate_image(self.return_objects()), reward, True
        self.prev_distance = prey_distance
        self.move_prey()

        return self.generate_image(self.return_objects()), reward, False

    #This function takes a list of objects and draws them, needs to be fixed to draw them in a certain order

    def draw_objects(self, objects, img):
        
        object = objects.pop()

        if len(objects) > 0:
            img = self.draw_objects(objects, img)

        distance_from_player = self.calculate_distance(object)
        if distance_from_player > 0.001:
            render_size = round(object.return_size() * (5.0 / distance_from_player))
            angle = self.calculate_angle(object)
            looking_angle = self.return_looking_angle()
            if looking_angle > 90 and angle < -90:
                angle += 360
            elif looking_angle < -90 and angle > 90:
                angle -= 360
            angle_difference = looking_angle - angle
            location = round(((angle_difference / 360) * (total_width)) + (width / 2))
            cv2.circle(img, [location, round(height / 2)], radius = render_size, color = object.return_color(), thickness = -1)
        
        return img

    #This function will take a list of objects and sort them in the order in which they should be rendered

    def sort_objects(self, objects):
        distances = []
        for object in objects:
            distances.append(self.calculate_distance(object))

        index = list(range(len(distances)))
        index.sort(key = distances.__getitem__)
        index.reverse()
        objects[:] = [objects[i] for i in index]

        return objects
    
    #This function will make the image using previous functions

    def generate_image(self, objects):

        img = np.zeros((height, width, 3), dtype=np.uint8)
        img = self.draw_objects(self.sort_objects(objects), img)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #This function will convert an image to a list of values

    def convert_image(self, img):
        img_list = img.tolist()
        final_list = []
        for i in range(len(img_list)):
            for j in range(len(img_list[i])):
                final_list.append(img_list[i][j] / 255.0)
        return final_list

    #This function combines the list of pixels with the list of previous actions

    def return_memory(self):
        
        memory = np.zeros(max_moves, dtype=np.float32).tolist()
        for i in range(len(self.memory)):
            memory[i] = self.memory[i] / 3.0

        return memory

    #This function returns the environment's discount

    def return_discount(self):
        return self.discount


#This class is for holding all the data of an object such as location, size, and color
#Color is in BGR

class Object:

    def __init__(self, location, size, color):
        self.location = location
        self.size = size
        self.color = color

    def return_location(self):
        return self.location

    def return_size(self):
        return self.size

    def return_color(self):
        return self.color


if __name__ == "__main__":

    env = HuntingEnvironment()
    while True:

        img = np.zeros((height, width, 3), dtype=np.uint8)
        img = env.draw_objects(env.sort_objects(env.return_objects()), img)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = cv2.resize(img, (1024, 512))
        cv2.imshow('Environment', img)

        cv2.waitKey(0)
        if kb.is_pressed("w"):
            env.run_frame(0)
        elif kb.is_pressed("s"):
            env.run_frame(1)
        elif kb.is_pressed("d"):
            env.run_frame(2)
        elif kb.is_pressed("a"):
            env.run_frame(3)
        elif kb.is_pressed("q"):
            break
    
    cv2.destroyAllWindows()


print ("Env Loaded Correctly !")