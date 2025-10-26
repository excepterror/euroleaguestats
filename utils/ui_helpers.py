from kivy.core.window import Window

def adaptive_height(scale, max_height):
    """Return a safe adaptive height value that scales with screen size."""
    try:
        height = getattr(Window, "height", None)
        '''If height is None or 0 (Window not ready yet), fallback.'''
        if not height or height <= 0:
            return max_height
        width, height = Window.size
        dpi = Window.dpi
        diagonal_in = ((width / dpi) ** 2 + (height / dpi) ** 2) ** 0.5
        '''Clamp values to avoid extremes.'''
        diagonal_in = max(4.5, min(diagonal_in, 12))
        '''Linear interpolation between 6" = 1.0 and 10" = 1.3.'''
        font_scale = 1.0 + 0.025 * (diagonal_in - 6)
        '''Cap font_scale.'''
        font_scale = min(height * scale * font_scale, max_height * font_scale)
        return font_scale
    except Exception:
        return max_height
