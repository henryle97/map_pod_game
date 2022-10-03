import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop

class Vector:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @staticmethod  
    def equal(a, b):
        return a.x == b.x and a.y == b.y 

    @staticmethod  
    def sum(a, b):
        return Vector(a.x + b.x, a.y + b.y) 

    @staticmethod  
    def sub(a, b):
        return Vector(a.x - b.x, a.y - b.y) 

    @staticmethod  
    def mul(k, a):
        return Vector(k * a.x, k* a.y) 

    @staticmethod  
    def distSqr(a, b):
        return (a.x - b.x)**2 + (a.y-b.y)**2


class CheckpointManager:
    def __init__(self):
        self.checkpoints = []
        self.current_lap = 0
        self.checkpoint_index = 0 
        self.best_boost_index = -1 


    def should_use_boost(self):
        return self.checkpoint_index == self.best_boost_index
    
    def update(self, next_checkpoint):

        # if not visited any checkpoint
        if len(self.checkpoints) == 0:
            self.checkpoints.append(next_checkpoint)
            return 0

        print(f"Lap {self.current_lap} - Index {self.checkpoint_index} - Boost index {self.best_boost_index}", file=sys.stderr, flush=True)

        # no update
        if Vector.equal(next_checkpoint, self.checkpoints[self.checkpoint_index]):
            return 0

        # end of the lap 
        if Vector.equal(next_checkpoint, self.checkpoints[0]):      
            if (self.current_lap == 0):  # know all the checkpoints
                self.compute_best_boost_index()
            
            self.current_lap += 1 
            self.checkpoint_index = 0
        # update checkpoint
        else:
            self.checkpoint_index += 1
            if self.current_lap == 0:
                self.checkpoints.append(next_checkpoint)

    def compute_best_boost_index(self):
        # compute the longest step 
        if len(self.checkpoints) == 2:
            return 0
        
        longest_dist = float('-inf')

        total_checkpoints = len(self.checkpoints)
        for checkpoint_index in range(total_checkpoints):
            next_checkpoint_index = (checkpoint_index + 1) % total_checkpoints
            current_dist = Vector.distSqr(self.checkpoints[checkpoint_index], self.checkpoints[next_checkpoint_index])

            if current_dist > longest_dist:
                self.best_boost_index = checkpoint_index
                longest_dist = current_dist

#global variables 
can_boost = True 
checkpoint_manager = CheckpointManager()

pre_pos = Vector(-1, -1)
init = False 
max_thrust = 100
checkpoint_radius_sqr = 360000

while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # You have to output the target position
    # followed by the power (0 <= thrust <= 100) or "BOOST"
    # i.e.: "x y thrust"

    
    # cal best next_checkpoint_x, next_checkpoint_y, thrush

    curr_pos = Vector(x, y)
    next_pos = Vector(next_checkpoint_x, next_checkpoint_y)
    angle = abs(next_checkpoint_angle)

    if pre_pos.x < 0:
        pre_pos = curr_pos
    
    checkpoint_manager.update(next_pos)

    target_pos = next_pos
    thrust = max_thrust
    use_boost = False 
    if angle < 1:
        thrust = max_thrust
        use_boost = can_boost and checkpoint_manager.should_use_boost()
    else:
        d_pos = Vector.sub(curr_pos, pre_pos)
        target = Vector.sub(target_pos, Vector.mul(3, d_pos))

        dist_to_target = Vector.distSqr(curr_pos, target_pos)
        dist_slowdown_factor = max(0, min(dist_to_target / (checkpoint_radius_sqr * 4), 1))
        angle_slowdown_factor = 1 - max(0, min(angle / 90, 1))
        thrust = int(max_thrust * dist_slowdown_factor * angle_slowdown_factor)

    # update value for next rurn 
    pre_pos = curr_pos 
    if (use_boost):
        can_boost = False 
    
    thrust_str = "BOOST" if use_boost else str(thrust)

    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + thrust_str)