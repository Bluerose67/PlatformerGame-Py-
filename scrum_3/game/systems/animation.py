import pygame

class Animation:
    def __init__(self, frames, frame_duration):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.timer = 0

    def current_image(self):
        return self.frames[self.current_frame]

class Animator:
    def __init__(self):
        self.animations = {}
        self.current_anim = None
        
    def add_animation(self, name, animation):
        self.animations[name] = animation
        
    def play(self, name):
        if self.current_anim != name:
            self.current_anim = name
            self.animations[name].current_frame = 0
            self.animations[name].timer = 0
            
    def get_current_frame(self):
        return self.animations[self.current_anim].current_image()