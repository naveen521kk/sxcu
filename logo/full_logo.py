import cairocffi as cairo
import pangocairocffi
import pangocffi
from thumbnail_logo import logo
sep_btn_lines= 0.5
logowidth= LOGOWIDTH = logoheight=LOGOHEIGHT = 5
width=WIDTH = 25
height=HEIGHT = 10
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
    layout.set_alignment(pangocffi.Alignment.CENTER)
    fontdesc = pangocffi.FontDescription()
    fontdesc.set_size(pangocffi.units_from_double(5))
    fontdesc.set_family(font_family)
    layout.set_font_description(fontdesc)
    layout.set_text(text)
    pangocairocffi.show_layout(ctx, layout)
background()
logo(ctx,start_y=height/2-logowidth+sep_btn_lines+1.5)
write_text(ctx,"SCXU",0,0)
surface.finish()

import os
os.startfile("full_logo.svg")

