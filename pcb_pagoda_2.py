from matplotlib import pylab
from pylab import *
import os
import mbpcb
import sys

if (sys.version_info.major != 3):
        print("ERROR: DO NOT USE python2, it will produce bad results")
        sys.exit(1)

#import imp
#imp.reload(mbpcb)

# for multi pcb:
global multi_pcb_spacing
global panel_count_x
global panel_count_y
panel_count_x = 4
panel_count_y = 3
multi_pcb_spacing = 24.5

#font = "fonts/Salsa.ttf"
font = "fonts/square_metall-7.ttf"

# simulation: balun-test-v12-l80.hfss

coax_r1 = 0.46
coax_r2 = 1.5
coax_r3 = 1.8
disk_r1 = 5.1539
disk_r2 = 7.5056
disk_r3 = 5.6459
disk_d1 = 3.6526 # pcb1 bot -> pcb2 top
disk_d2 = 12.4514 # pcb2 top -> pcb3 bot
pcb_th = 1.0 # fr4 core only, not including copper or solder mask
track_w1 = 1.0
track_w2 = 1.0
track_a1 = 71.7938
track_c1 = 17.49
track_r1 = 10.2313
track_r2 = 8.6079
solder_w = 0.6
ring_w = 0.25 # via_w in simulation
hole_sp = 0.05 # for coax core
hole_sp2 = 0.1 # for coax shield, larger because more variation here
mask_sp = 0.1
hole_r1 = 2.3863
hole_r2 = 5.2364

pcb_r1 = track_r1 + track_w1 / 2 + 0.5
pcb_r2 = track_r1 + track_w1 / 2 + 0.5
pcb_r3 = disk_r3 + 0.5
track_b1 = -track_c1/2

oshw_x = array([
         0.28885504,  0.10469736,  0.13888441,  0.17044261,  0.19877461,  0.22334415,  0.24368615,  0.25941557,
         0.27023469,  0.27593872,  0.27641969,  0.27166849,  0.26177506,  0.24692667,  0.22740436,  0.20357767,
         0.17589759,  0.14488807,  0.11113605,  0.07528041,  0.03799984,  0.        , -0.03799984, -0.07528041,
        -0.11113605, -0.14488807, -0.17589759, -0.20357767, -0.22740436, -0.24692667, -0.26177506, -0.27166849,
        -0.27641969, -0.27593872, -0.27023469, -0.25941557, -0.24368615, -0.22334415, -0.19877461, -0.17044261,
        -0.13888441, -0.10469736, -0.28885504, -0.38204406, -0.60348636, -0.79737332, -0.64548688, -0.7265741 ,
        -0.99055738, -0.99055738, -0.7265741 , -0.64548688, -0.79737332, -0.60348636, -0.38204406, -0.1862822 ,
        -0.13709878,  0.13709878,  0.1862822 ,  0.38204406,  0.60348636,  0.79737332,  0.64548688,  0.7265741 ,
         0.99055738,  0.99055738,  0.7265741 ,  0.64548688,  0.79737332,  0.60348636,  0.38204406,
])
oshw_y = array([
        -0.70711199, -0.25629728, -0.23950146, -0.21817229, -0.19271348, -0.16360692, -0.13140355, -0.09671293,
        -0.0601917 , -0.02253114,  0.01555589,  0.05334848,  0.09013127,  0.12520803,  0.15791481,  0.18763252,
         0.21379866,  0.23591795,  0.2535717 ,  0.26642577,  0.27423684,  0.27685706,  0.27423684,  0.26642577,
         0.2535717 ,  0.23591795,  0.21379866,  0.18763252,  0.15791481,  0.12520803,  0.09013127,  0.05334848,
         0.01555589, -0.02253114, -0.0601917 , -0.09671293, -0.13140355, -0.16360692, -0.19271348, -0.21817229,
        -0.23950146, -0.25629728, -0.70711199, -0.64548688, -0.79737332, -0.60348636, -0.38204406, -0.1862822 ,
        -0.13709878,  0.13709878,  0.1862822 ,  0.38204406,  0.60348636,  0.79737332,  0.64548688,  0.7265741 ,
         0.99055738,  0.99055738,  0.7265741 ,  0.64548688,  0.79737332,  0.60348636,  0.38204406,  0.1862822 ,
         0.13709878, -0.13709878, -0.1862822 , -0.38204406, -0.60348636, -0.79737332, -0.64548688,
])

def polygon_arc(shapes, cx, cy, radius, angle):
        res = []
        for shape in shapes:
                if shape["type"] == "polygon":
                        r = radius + shape["y"]
                        theta = angle * pi / 180 - shape["x"] / radius
                        (shape["x"], shape["y"]) = (cx + r * cos(theta), cy + r * sin(theta))

@mbpcb.register
def pcb1(pol, mouse_bites):
        global multi_pcb_spacing
        global panel_x
        global panel_y
        global panel_count_x
        global panel_count_y
        shapes = []
        #shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r1, outline=0.1)
        outline_w = 0.1
        arc_gap   = 15
        bar_len   = (multi_pcb_spacing - 2*pcb_r1) / 2 + 2 * outline_w
        breakaway_hole_dia = 0.35
        breakaway_hole_spacing = breakaway_hole_dia + 0.3
        for apos in range(4):
                arc_shape = mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+arc_gap/2, apos*90+90-arc_gap/2, outline=outline_w)
                shapes += arc_shape
                #extract start and endpoint of arc
                arc = [ [arc_shape[0]["x"][0], arc_shape[0]["y"][0]], [arc_shape[0]["x"][-1], arc_shape[0]["y"][-1]]]
                #add bar and cut holes
                if (apos == 0):
                        dir_x = 1
                        dir_y = 0
                elif (apos == 1):
                        dir_x = 0
                        dir_y = 1
                elif (apos == 2):
                        dir_x = -1
                        dir_y = 0
                else:
                        dir_x = 0
                        dir_y = -1
                
                #add bar
                if (panel_x == 0 and panel_y == 0 ):
                        if (apos == 0):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == (panel_count_x-1) and panel_y == 0 ):
                        if (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == (panel_count_x-1) and panel_y == (panel_count_y -1) ):
                        if (apos == 1 or apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == 0 and panel_y == (panel_count_y -1) ):
                        if (apos == 0 or apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == 0 and panel_y != 0 and panel_y != (panel_count_y -1)):
                        if (apos == 0 or apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == (panel_count_x-1) and panel_y != 0 and panel_y != (panel_count_y -1)):
                        if (apos == 1 or apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_y == 0 and panel_x != 0 and panel_x != (panel_count_x -1)):
                        if (apos == 0 or apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_y == (panel_count_y -1) and panel_x != 0 and panel_x != (panel_count_x -1)):
                        if (apos == 2 or apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x != 0 and panel_x != (panel_count_x -1) and panel_y != 0 and panel_y != (panel_count_y -1)):
                        #line at start of arc
                        shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        #line at end of arc
                        shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)

                #cut holes
                if (mouse_bites == "yes"):
                        if (panel_x == 0 and panel_y == 0 and apos != 3 and apos != 2):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == (panel_count_x-1) and panel_y == 0 and apos != 3 and apos != 0):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == (panel_count_x-1) and panel_y == (panel_count_y -1) and apos != 0):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == 0 and panel_y == (panel_count_y -1) and apos != 2):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == 0 and panel_y != 0 and panel_y != (panel_count_y -1) and apos != 2):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == (panel_count_x-1) and panel_y != 0 and panel_y != (panel_count_y -1) and apos != 0):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_y == 0 and panel_x != 0 and panel_x != (panel_count_x -1) and apos != 3):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_y == (panel_count_y -1) and panel_x != 0 and panel_x != (panel_count_x -1) and apos != 1):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x != 0 and panel_x != (panel_count_x -1) and panel_y != 0 and panel_y != (panel_count_y -1)):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                                
                #close sides
                if (panel_x == 0):
                        if (apos == 2):
                                #close left side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 1):
                                #close left side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                elif (panel_x == (panel_count_x-1)):
                        if (apos == 0):
                                #close right side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 3):
                                #close right side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                                
                if (panel_y == 0):
                        if (apos == 3):
                                #close bot
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 2):
                                #close bot
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                elif (panel_y == (panel_count_y -1) and panel_x != 0 and panel_x != panel_count_x-1):
                        if (apos == 1):
                                #close top
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 0):
                                #close top
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
        
        # coax connection
        shapes += mbpcb.make_circle("drill-plated", 0.0, 0.0, coax_r1 + hole_sp, pad=True)
        shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, coax_r1 + solder_w)
        shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r3 + solder_w, pad=True)
        shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r2, hole=True, pad=True)
        shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r1 + hole_sp + ring_w, pad=True, order=1)
        shapes += mbpcb.make_circle("mask-top", 0.0, 0.0, coax_r1 + solder_w + mask_sp)
        shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
        shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r2 - mask_sp, hole=True, pad=True)
        shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r1 + hole_sp + ring_w + mask_sp, pad=True, order=1)
        
        # ring
        #shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, (hole_r1 + disk_r1) / 2, 0.0, 360.0, outline=disk_r1 - hole_r1)
        shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, (hole_r1 + disk_r1) / 2, outline=disk_r1 - hole_r1)
        
        # legs
        for angle in arange(3) * 120 + 90:
                if pol == "LHCP":
                        a1 = angle + track_b1 - (track_w2 - track_w1) / 2.0 / track_r1
                        a2 = a1 + track_a1
                        a3 = angle + track_b1
                        a4 = angle + track_b1 + track_c1
                else:
                        a1 = angle - track_b1 + (track_w2 - track_w1) / 2.0 / track_r1
                        a2 = a1 - track_a1
                        a3 = angle - track_b1
                        a4 = angle - track_b1 - track_c1
                a5 = angle + 60.0
                shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r1, a1, a2, outline=track_w1)
                shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r2, a3, a4, outline=track_w1)
                shapes += mbpcb.make_line("copper1-top",
                                track_r1 * cos(a3 * pi/180), track_r1 * sin(a3 * pi/180),
                                track_r2 * cos(a3 * pi/180), track_r2 * sin(a3 * pi/180), outline=track_w2)
                shapes += mbpcb.make_line("copper1-top",
                                disk_r1  * cos(a4 * pi/180), disk_r1  * sin(a4 * pi/180),
                                track_r2 * cos(a4 * pi/180), track_r2 * sin(a4 * pi/180), outline=track_w2)
                shapes += mbpcb.make_line("copper1-top", 0.0, 0.0,
                                hole_r1 * cos(a5 * pi/180), hole_r1 * sin(a5 * pi/180), outline=track_w2)
                shapes += mbpcb.make_line("silk-top",
                                track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
                                track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
                shapes += mbpcb.make_line("silk-bot",
                                track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
                                track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
        
        # text
        shapes += mbpcb.make_text("silk-top", font, pol, 1.8,
                        0.0, 7.5, align="center", valign="center", spacing=0.05)
        shapes += mbpcb.make_text("silk-top", font, "Pagoda-2", 3.0,
                        0.0, 5.0, align="center", valign="center", spacing=0.05)
        shapes += mbpcb.make_text("silk-top", font, "Designed by", 1.8,
                        0.0, -4.0, align="center", valign="center", spacing=0.05)
        shapes += mbpcb.make_text("silk-top", font, "Maarten", 1.8,
                        0.0, -6.0, align="center", valign="center", spacing=0.05)
        shapes += mbpcb.make_text("silk-top", font, "Baert", 1.8,
                        0.0, -8.0, align="center", valign="center", spacing=0.05)

        return shapes

@mbpcb.register
def pcb2(pol, mouse_bites):
        #shapes = []
        #shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r1, outline=0.1)
        
        global multi_pcb_spacing
        global panel_x
        global panel_y
        global panel_count_x
        global panel_count_y
        shapes = []
        #shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r1, outline=0.1)
        outline_w = 0.1
        arc_gap   = 15
        bar_len   = (multi_pcb_spacing - 2*pcb_r1) / 2 + 2 * outline_w
        breakaway_hole_dia = 0.35
        breakaway_hole_spacing = breakaway_hole_dia + 0.3
        for apos in range(4):
                arc_shape = mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+arc_gap/2, apos*90+90-arc_gap/2, outline=outline_w)
                shapes += arc_shape
                #extract start and endpoint of arc
                arc = [ [arc_shape[0]["x"][0], arc_shape[0]["y"][0]], [arc_shape[0]["x"][-1], arc_shape[0]["y"][-1]]]
                #add bar and cut holes
                if (apos == 0):
                        dir_x = 1
                        dir_y = 0
                elif (apos == 1):
                        dir_x = 0
                        dir_y = 1
                elif (apos == 2):
                        dir_x = -1
                        dir_y = 0
                else:
                        dir_x = 0
                        dir_y = -1
                        
                #add bar
                if (panel_x == 0 and panel_y == 0 ):
                        if (apos == 0):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == (panel_count_x-1) and panel_y == 0 ):
                        if (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == (panel_count_x-1) and panel_y == (panel_count_y -1) ):
                        if (apos == 1 or apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == 0 and panel_y == (panel_count_y -1) ):
                        if (apos == 0 or apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == 0 and panel_y != 0 and panel_y != (panel_count_y -1)):
                        if (apos == 0 or apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x == (panel_count_x-1) and panel_y != 0 and panel_y != (panel_count_y -1)):
                        if (apos == 1 or apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_y == 0 and panel_x != 0 and panel_x != (panel_count_x -1)):
                        if (apos == 0 or apos == 1):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_y == (panel_count_y -1) and panel_x != 0 and panel_x != (panel_count_x -1)):
                        if (apos == 2 or apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 0):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        elif (apos == 1):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                if (panel_x != 0 and panel_x != (panel_count_x -1) and panel_y != 0 and panel_y != (panel_count_y -1)):
                        #line at start of arc
                        shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        #line at end of arc
                        shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)

                #cut holes
                if (mouse_bites == "yes"):
                        if (panel_x == 0 and panel_y == 0 and apos != 3 and apos != 2):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == (panel_count_x-1) and panel_y == 0 and apos != 3 and apos != 0):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == (panel_count_x-1) and panel_y == (panel_count_y -1) and apos != 0):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == 0 and panel_y == (panel_count_y -1) and apos != 2):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == 0 and panel_y != 0 and panel_y != (panel_count_y -1) and apos != 2):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == (panel_count_x-1) and panel_y != 0 and panel_y != (panel_count_y -1) and apos != 0):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_y == 0 and panel_x != 0 and panel_x != (panel_count_x -1) and apos != 3):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_y == (panel_count_y -1) and panel_x != 0 and panel_x != (panel_count_x -1) and apos != 1):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x != 0 and panel_x != (panel_count_x -1) and panel_y != 0 and panel_y != (panel_count_y -1)):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                                
                #close sides
                if (panel_x == 0):
                        if (apos == 2):
                                #close left side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 1):
                                #close left side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                elif (panel_x == (panel_count_x-1)):
                        if (apos == 0):
                                #close right side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 3):
                                #close right side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                                
                if (panel_y == 0):
                        if (apos == 3):
                                #close bot
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 2):
                                #close bot
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                elif (panel_y == (panel_count_y -1) and panel_x != 0 and panel_x != panel_count_x-1):
                        if (apos == 1):
                                #close top
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 0):
                                #close top
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r1, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
        
        
        # coax connection
        shapes += mbpcb.make_circle("drill-plated", 0.0, 0.0, coax_r3 + hole_sp2, pad=True)
        shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, coax_r3 + solder_w, pad=True)
        shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r3 + solder_w, pad=True)
        shapes += mbpcb.make_circle("mask-top", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
        shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
        
        # ring
        #shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, (hole_r2 + disk_r2) / 2, 0.0, 360.0, outline=disk_r2 - hole_r2)
        shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, (hole_r2 + disk_r2) / 2, outline=disk_r2 - hole_r2)
        
        # legs
        for angle in arange(3) * 120 + 90:
                if pol == "LHCP":
                        a1 = angle - track_b1 + (track_w2 - track_w1) / 2.0 / track_r1
                        a2 = a1 - track_a1
                        a3 = angle - track_b1
                        a4 = angle - track_b1 - track_c1
                else:
                        a1 = angle + track_b1 - (track_w2 - track_w1) / 2.0 / track_r1
                        a2 = a1 + track_a1
                        a3 = angle + track_b1
                        a4 = angle + track_b1 + track_c1
                a5 = angle + 60.0
                shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r1, a1, a2, outline=track_w1)
                shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r2, a3, a4, outline=track_w1)
                shapes += mbpcb.make_line("copper1-top",
                                track_r1 * cos(a3 * pi/180), track_r1 * sin(a3 * pi/180),
                                track_r2 * cos(a3 * pi/180), track_r2 * sin(a3 * pi/180), outline=track_w2)
                shapes += mbpcb.make_line("copper1-top",
                                disk_r2  * cos(a4 * pi/180), disk_r2  * sin(a4 * pi/180),
                                track_r2 * cos(a4 * pi/180), track_r2 * sin(a4 * pi/180), outline=track_w2)
                shapes += mbpcb.make_line("copper1-top", 0.0, 0.0,
                                hole_r2 * cos(a5 * pi/180), hole_r2 * sin(a5 * pi/180), outline=track_w2)
                shapes += mbpcb.make_line("silk-top",
                                track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
                                track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
                shapes += mbpcb.make_line("silk-bot",
                                track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
                                track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
        
        # OSHW logo
        shapes += mbpcb.make_polygon("silk-bot", 1.8 * oshw_x, 1.8 * oshw_y + 5.8)
        
        # text
        shapes2 = mbpcb.make_text("silk-top", font, "Pagoda-2 · 5.8GHz · " + pol + " · CC BY-SA", 2.0,
                                0.0, 0.0, align="center", valign="center", spacing=-0.10)
        polygon_arc(shapes2, 0.0, 0.0, 6.1, -90.0)
        mbpcb.pcb_transform(shapes2, 0.0, 0.0, 0.0, 0.0, 0.0, True)
        shapes += shapes2
        
        return shapes

@mbpcb.register
def pcb3(mouse_bites):
        #shapes = []
        #shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r3, outline=0.1)
        global multi_pcb_spacing
        global panel_x
        global panel_y
        global panel_count_x
        global panel_count_y
        shapes = []
        #shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r1, outline=0.1)
        outline_w = 0.1
        arc_gap   = 1.84*15
        bar_len   = (multi_pcb_spacing*.6 - 2*pcb_r3) / 2 + 2 * outline_w
        bar_len2   = (multi_pcb_spacing - 2*pcb_r3) / 2 + 2 * outline_w
        breakaway_hole_dia = 0.35
        breakaway_hole_spacing = breakaway_hole_dia + 0.3
        for apos in range(4):
                arc_shape = mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90+arc_gap/2, apos*90+90-arc_gap/2, outline=outline_w)
                shapes += arc_shape
                #extract start and endpoint of arc
                arc = [ [arc_shape[0]["x"][0], arc_shape[0]["y"][0]], [arc_shape[0]["x"][-1], arc_shape[0]["y"][-1]]]
                #add bar and cut holes
                if (apos == 0):
                        dir_x = 1
                        dir_y = 0
                elif (apos == 1):
                        dir_x = 0
                        dir_y = 1
                elif (apos == 2):
                        dir_x = -1
                        dir_y = 0
                else:
                        dir_x = 0
                        dir_y = -1

                #add bar
                if (panel_x == 0 and panel_y == 3):
                        if (apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len2, arc[0][1] + dir_y*bar_len2, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 2):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len2, arc[1][1] + dir_x*bar_len2, outline=outline_w)
                        elif (apos == 0):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                elif (panel_x == 5 and panel_y == 3):
                        if (apos == 2):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len2, arc[1][1] + dir_x*bar_len2, outline=outline_w)
                        elif (apos == 1):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        elif (apos == 3):
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len2, arc[0][1] + dir_y*bar_len2, outline=outline_w)
                else:
                        if (apos == 1 or apos == 3):
                                #line at end of arc
                                shapes += mbpcb.make_line("board-outline", arc[1][0], arc[1][1], arc[1][0] - dir_y*bar_len, arc[1][1] + dir_x*bar_len, outline=outline_w)
                        else:
                                #line at start of arc
                                shapes += mbpcb.make_line("board-outline", arc[0][0], arc[0][1], arc[0][0] + dir_x*bar_len, arc[0][1] + dir_y*bar_len, outline=outline_w)
                        
                #cut holes
                if (mouse_bites == "yes"):
                        if (panel_x == 0 and panel_y == 3 and apos != 1 and apos != 2):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_x == 5 and panel_y == 3 and apos != 0 and apos != 1):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                        elif (panel_y == 3 and panel_x != 0 and panel_x != 5 and apos != 1 and apos != 3):
                                for hole in range(4):
                                        shapes += mbpcb.make_circle("drill-plated", 
                                                arc[0][0] + dir_x * 1.1 * breakaway_hole_dia + dir_y * (hole + 0.6) * breakaway_hole_spacing, 
                                                arc[0][1] + dir_y * 1.1 * breakaway_hole_dia - dir_x * (hole + 0.6) * breakaway_hole_spacing, 
                                                breakaway_hole_dia/2, pad=False)
                #close sides
                if (panel_x == 0):
                        if (apos == 2):
                                #close left side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 1):
                                #close left side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                elif (panel_x == 5):
                        if (apos == 0):
                                #close right side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 3):
                                #close right side
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                                
                if (panel_y == 3 and panel_x != 0 and panel_x != 5):
                        if (apos == 3):
                                #close bot
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 2):
                                #close bot
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
                if (panel_y == 3):
                        if (apos == 1):
                                #close top
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90, apos*90+arc_gap/2, outline=outline_w)
                        elif (apos == 0):
                                #close top
                                shapes += mbpcb.make_arc("board-outline", 0.0, 0.0, pcb_r3, apos*90+90-arc_gap/2, apos*90+90, outline=outline_w)
        
        
        # coax connection
        shapes += mbpcb.make_circle("drill-plated", 0.0, 0.0, coax_r3 + hole_sp2, pad=True)
        shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, coax_r3 + solder_w, pad=True)
        shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r3 + solder_w, pad=True)
        shapes += mbpcb.make_circle("mask-top", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
        shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
        
        # disk
        shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, disk_r3)
        
        # text
        shapes2 = mbpcb.make_text("silk-top", font, "Pagoda-2 · OSHW · CC BY-SA", 2.0,
                        0.0, 0.0, align="center", valign="center", spacing=-0.10)
        polygon_arc(shapes2, 0.0, 0.0, 4.25, -90.0)
        shapes3 = mbpcb.make_text("silk-top", font, "·", 2.0,
                        0.0, 0.0, align="center", valign="center", spacing=-0.10)
        polygon_arc(shapes3, 0.0, 0.0, 4.25, 90.0)
        mbpcb.pcb_transform(shapes2, 0.0, 0.0, 0.0, 0.0, 0.0, True)
        mbpcb.pcb_transform(shapes3, 0.0, 0.0, 0.0, 0.0, 0.0, True)
        shapes += shapes2 + shapes3
        
        return shapes


shapes = []
panel_x = 0
panel_y = 0
shapes += mbpcb.place("pcb1", -12.5,  12.5, 0.0, False, pol="LHCP", mouse_bites="yes")
shapes += mbpcb.place("pcb1",  12.5,  12.5, 0.0, False, pol="RHCP", mouse_bites="yes")
shapes += mbpcb.place("pcb2", -12.5, -12.5, 0.0, False, pol="LHCP", mouse_bites="yes")
shapes += mbpcb.place("pcb2",  12.5, -12.5, 0.0, False, pol="RHCP", mouse_bites="yes")
shapes += mbpcb.place("pcb3",  0.0, 0.0, 0.0, False, mouse_bites="yes")

close("all")
#mbpcb.pcb_plot("Pagoda", shapes)
##mbpcb.pcb_plot("Pagoda Top", shapes, layers=[l for l in mbpcb.layerstack if not l.endswith("-bot")])
##mbpcb.pcb_plot("Pagoda Bot", shapes, layers=[l for l in mbpcb.layerstack if not l.endswith("-top")])

basepath = os.path.dirname(os.path.realpath(__file__)) + "/gerber"

#6 x RHCP part123
shapes = []
for panel_x in range(panel_count_x):
        for panel_y in range(panel_count_y):
                if (panel_x%2 == 0):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="yes")
                else:
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="yes")
panel_y += 1
for panel_x in range(6):
        shapes += mbpcb.place("pcb3", panel_x*multi_pcb_spacing*.6, panel_y*multi_pcb_spacing, 0.0, False, mouse_bites ="yes")

mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_2_part123_rhcp")

#6 x LHCP part123
shapes = []
for panel_x in range(panel_count_x):
        for panel_y in range(panel_count_y):
                if (panel_x%2 == 0):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="yes")
                else:
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="yes")
panel_y += 1
for panel_x in range(6):
        shapes += mbpcb.place("pcb3", panel_x*multi_pcb_spacing*.6, panel_y*multi_pcb_spacing, 0.0, False, mouse_bites ="yes")

mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_2_part123_lhcp")

#3 x RHCP + 3 x LHCP part123
shapes = []
for panel_x in range(panel_count_x):
        for panel_y in range(panel_count_y):
                if (panel_x == 0):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="yes")
                elif (panel_x == 1):
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="yes")
                elif (panel_x == 2):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="yes")
                elif (panel_x == 3):
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="yes")
panel_y += 1
for panel_x in range(6):
        shapes += mbpcb.place("pcb3", panel_x*multi_pcb_spacing*.6, panel_y*multi_pcb_spacing, 0.0, False, mouse_bites ="yes")

mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_2_part123_rlhcp")



#6 x RHCP part123
shapes = []
for panel_x in range(panel_count_x):
        for panel_y in range(panel_count_y):
                if (panel_x%2 == 0):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="no")
                else:
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="no")
panel_y += 1
for panel_x in range(6):
        shapes += mbpcb.place("pcb3", panel_x*multi_pcb_spacing*.6, panel_y*multi_pcb_spacing, 0.0, False, mouse_bites ="no")

mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_2_part123_rhcp_nomousebites")

#6 x LHCP part123
shapes = []
for panel_x in range(panel_count_x):
        for panel_y in range(panel_count_y):
                if (panel_x%2 == 0):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="no")
                else:
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="no")
panel_y += 1
for panel_x in range(6):
        shapes += mbpcb.place("pcb3", panel_x*multi_pcb_spacing*.6, panel_y*multi_pcb_spacing, 0.0, False, mouse_bites ="no")

mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_2_part123_lhcp_nomousebites")

#3 x RHCP + 3 x LHCP part123
shapes = []
for panel_x in range(panel_count_x):
        for panel_y in range(panel_count_y):
                if (panel_x == 0):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="no")
                elif (panel_x == 1):
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="RHCP", mouse_bites ="no")
                elif (panel_x == 2):
                        shapes += mbpcb.place("pcb1", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="no")
                elif (panel_x == 3):
                        shapes += mbpcb.place("pcb2", panel_x*multi_pcb_spacing, panel_y*multi_pcb_spacing, 0.0, False, pol="LHCP", mouse_bites ="no")
panel_y += 1
for panel_x in range(6):
        shapes += mbpcb.place("pcb3", panel_x*multi_pcb_spacing*.6, panel_y*multi_pcb_spacing, 0.0, False, mouse_bites ="no")

mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_2_part123_rlhcp_nomousebites")
