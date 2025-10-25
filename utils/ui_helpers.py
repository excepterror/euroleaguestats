from kivy.core.window import Window

def adaptive_height(scale, max_height):
    """Return a safe adaptive height value that scales with screen size."""
    try:
        height = getattr(Window, "height", None)
        '''If height is None or 0 (Window not ready yet), fallback.'''
        if not height or height <= 0:
            return max_height
        return min(height * scale, max_height)
    except Exception:
        return max_height
