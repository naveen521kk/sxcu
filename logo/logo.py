import cairocffi as cairo

width=WIDTH = height=HEIGHT = 5
PIXEL_SCALE = 100

surface = cairo.SVGSurface("thumbnail_logo.svg",WIDTH*PIXEL_SCALE,HEIGHT*PIXEL_SCALE)
ctx = cairo.Context(surface)
ctx.scale(PIXEL_SCALE,PIXEL_SCALE)

#text_color = 1,1,1
text_color = 0,0,0


#logo samll rectangle
ctx.set_line_width(0.06)
ctx.move_to(2,2)
ctx.line_to(3,2)
ctx.line_to(3,3)
ctx.line_to(2,3)
ctx.close_path()
ctx.set_source_rgb(*text_color)
ctx.stroke()

# logo outer cover
sep_btn_lines=0.5
ctx.move_to(sep_btn_lines,sep_btn_lines)
ctx.line_to(width-sep_btn_lines,sep_btn_lines)
ctx.line_to(width-(sep_btn_lines*2),sep_btn_lines*2)
ctx.line_to(sep_btn_lines*2,sep_btn_lines*2)
ctx.line_to(sep_btn_lines*2,width-(sep_btn_lines)*2)
ctx.line_to(width-(sep_btn_lines*2),width-(sep_btn_lines)*2)
ctx.line_to(width-sep_btn_lines,width-sep_btn_lines)
ctx.line_to(sep_btn_lines,width-sep_btn_lines)
ctx.close_path()
ctx.stroke()    


import os
os.startfile("logo.svg")

