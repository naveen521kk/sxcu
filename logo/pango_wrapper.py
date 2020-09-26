import cffi

ffi = cffi.FFI()
ffi.cdef('''
    /* GLib */
    typedef void cairo_t;
    typedef void* gpointer;
    void g_object_unref (gpointer object);

    /* Pango and PangoCairo */
    typedef ... PangoLayout;
    typedef enum {
        PANGO_ALIGN_LEFT,
        PANGO_ALIGN_CENTER,
        PANGO_ALIGN_RIGHT
    } PangoAlignment;
    int pango_units_from_double (double d);
    PangoLayout * pango_cairo_create_layout (cairo_t *cr);
    void pango_cairo_show_layout (cairo_t *cr, PangoLayout *layout);
    void pango_layout_set_width (PangoLayout *layout, int width);
    void pango_layout_set_alignment (
        PangoLayout *layout, PangoAlignment alignment);
    void pango_layout_set_markup (
        PangoLayout *layout, const char *text, int length);
''')
gobject = ffi.dlopen('libgobject-2.0-0')
pango = ffi.dlopen('libpango-1.0-0')
pangocairo = ffi.dlopen('libpangocairo-1.0-0')


def gobject_ref(pointer):
    return ffi.gc(pointer, gobject.g_object_unref)


units_from_double = pango.pango_units_from_double
