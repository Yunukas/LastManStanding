import arcade

class MovingChar(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()

        self.texture_change_distance = 20
        self.movementSpeed = 0
        self.jumpSpeed = 0
        self.scale = 1

        self.stand_right_textures = []
        self.stand_left_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []

        # def setSpeed(self, speed):
        #     self.movementSpeed = speed
    
        # def setJumpSpeed(self, jumpSpeed):
        #     self.jumpSpeed = jumpSpeed
    
        # def setTextureChangeDistance(self, tcd):
        #     self.texture_change_distance = tcd   
        
        # def setScaling(self, scale):
        #     self.scale = scale

    # def changeDir(self):
    #     self.change_x *= -1

    def update(self):
        pass    
