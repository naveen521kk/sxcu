import cairocffi as cairo

def logo(ctx,sep_btn_lines=0.5,width=5,height=5,square_width=1,start_x=0,start_y=0):
    text_color = 1,1,1
    if __name__ == "__main__":
        text_color = 0,0,0
    #logo samll rectangle
    ctx.set_line_width(0.06)
    ctx.move_to(start_x+(width/2)-(square_width/2),start_y+(height/2)-(square_width/2))
    ctx.line_to(start_x+(width/2)-(square_width/2) +1 ,start_y+(height/2)-(square_width/2))
    ctx.line_to(start_x+(width/2)-(square_width/2) +1 ,start_y+(height/2)-(square_width/2) +1)
    ctx.line_to(start_x+(width/2)-(square_width/2),start_y+(height/2)-(square_width/2) +1)
    ctx.close_path()
    ctx.set_source_rgb(*text_color)
    ctx.stroke()

    # logo outer cover
    
    ctx.move_to(start_x+sep_btn_lines,start_y+sep_btn_lines)
    ctx.line_to(start_x+width-sep_btn_lines,start_y+sep_btn_lines)
    ctx.line_to(start_x+width-(sep_btn_lines*2),start_y+sep_btn_lines*2)
    ctx.line_to(start_x+sep_btn_lines*2,start_y+sep_btn_lines*2)
    ctx.line_to(start_x+sep_btn_lines*2,start_y+width-(sep_btn_lines)*2)
    ctx.line_to(start_x+width-(sep_btn_lines*2),start_y+width-(sep_btn_lines)*2)
    ctx.line_to(start_x+width-sep_btn_lines,start_y+width-sep_btn_lines)
    ctx.line_to(start_x+sep_btn_lines,start_y+width-sep_btn_lines)
    ctx.close_path()
    ctx.set_source_rgb(*text_color)
    ctx.stroke()    


if __name__ == "__main__":
    width=WIDTH = height=HEIGHT = 5
    PIXEL_SCALE = 100
    
    surface = cairo.SVGSurface("thumbnail_logo.svg",WIDTH*PIXEL_SCALE,HEIGHT*PIXEL_SCALE)
    ctx = cairo.Context(surface)
    ctx.scale(PIXEL_SCALE,PIXEL_SCALE)
    logo(ctx)
    import os
    os.startfile("thumbnail_logo.svg")

