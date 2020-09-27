"""
    :copyright: Copyright 2020 by Naveen M K
    :license: Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0). See https://creativecommons.org/licenses/by-nc-nd/4.0/ for more information.
"""
# Copyright 2020 Naveen M K
# Thanks to Merienda licensed under SIL OPEN FONT LICENSE Version 1.1. SEE LICENSE.FONT for More details.

import cairocffi as cairo
import pangocairocffi
import pangocffi
from thumbnail_logo import logo
sep_btn_lines= 0.5
logowidth= LOGOWIDTH = logoheight=LOGOHEIGHT = 5
width=WIDTH = 30
height=HEIGHT = 20
PIXEL_SCALE = 100
font_family="Merienda"
surface = cairo.SVGSurface("full_logo.svg",WIDTH*PIXEL_SCALE,HEIGHT*PIXEL_SCALE)
ctx = cairo.Context(surface)
ctx.scale(PIXEL_SCALE,PIXEL_SCALE)

# background
def background():
    ctx.rectangle(0,0,width,height)
    pattern = cairo.LinearGradient(0, 0, width, height)
    pattern.add_color_stop_rgb(0.2, (76/255), (40/255), (156/255)) #76,40,156
    pattern.add_color_stop_rgb(1, 223/255 , 153 /255, 216/255) #223,153,216
    ctx.set_source(pattern)
    ctx.fill()
def write_text(ctx,text,start_x,start_y):    
    ctx.move_to(start_x,start_y)
    layout = pangocairocffi.create_layout(ctx)
    layout.set_width(pangocffi.units_from_double(width))
    #layout.set_alignment(pangocffi.Alignment.CENTER)
    fontdesc = pangocffi.FontDescription()
    fontdesc.set_size(pangocffi.units_from_double(3))
    fontdesc.set_family(font_family)
    layout.set_font_description(fontdesc)
    layout.set_text(text)
    pangocairocffi.show_layout(ctx, layout)
background()
logo(ctx,start_x=sep_btn_lines*12,start_y=height/2-logowidth+sep_btn_lines+1.4)
print(ctx.path_extents())

write_text(ctx,"SXCU",sep_btn_lines*12+5+0.5,height/2-logowidth+sep_btn_lines+0.9)
surface.write_to_png("full_logo.png")
surface.finish()

import os
os.startfile("full_logo.svg")

