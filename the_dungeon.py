import sys
import time
import IPython

import world
from creatures import Player
from AI.player_ai import PlayerAI, DoorCompetentAI
import display
import rooms



def run(world, steps=None, slp=0.25, show=True, player=None):
    if steps is None:
        steps = sys.maxsize
    display.initialize()
    for i in range(steps):
        if show:
            to_display = [world]
            if player is not None and hasattr(player, "ai"):
                to_display.append(player.ai.model)
                to_display.append(player.percept())
                centers = [player.location,
                           player.ai.self_model.location,
                           (0,0)]
                score = player.score
            else:
                centers = [None]
                score = ""
            display.display(i, score, centers, 5, *to_display)
            time.sleep(slp)
        t = time.time()
        world.step()
        print(time.time() - t)



if __name__ == "__main__":
    dungeon = world.World()
    player = Player(dungeon, (9,2), DoorCompetentAI, direction=(0,1))
    #player = Player(dungeon, (9,2), PlayerAI, direction=(0,1))
    #rooms.testing_room(dungeon)
    #run(dungeon, player=player)
    rooms.three_doors(dungeon)
    #IPython.embed()
    run(dungeon)
