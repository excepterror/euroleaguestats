from kivy.core.window import Window
from math import sqrt
import sys

def get_screen_diagonal_in():
    """
    Returns the approximate physical screen diagonal in inches.
    Uses Android API if on Android, otherwise falls back to Kivy's Window.dpi.
    """
    '''Android platform.'''
    if sys.platform == 'android':
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            DisplayMetrics = autoclass('android.util.DisplayMetrics')

            activity = PythonActivity.mActivity
            metrics = DisplayMetrics()
            activity.getWindowManager().getDefaultDisplay().getMetrics(metrics)

            width_px = metrics.widthPixels
            height_px = metrics.heightPixels
            xdpi = metrics.xdpi
            ydpi = metrics.ydpi

            diagonal_in = sqrt((width_px / xdpi) ** 2 + (height_px / ydpi) ** 2)
            return diagonal_in
        except Exception as e:
            print("Warning: Android API failed, fallback to Kivy Window.dpi:", e)

    '''Non-Android fallback (desktop or other platforms)'''
    width_px, height_px = Window.size
    '''default mdpi fallback.'''
    dpi = getattr(Window, 'dpi', 160)
    density = getattr(Window, 'density', 1)
    if dpi <= 0:
        dpi = 160
    dpi *= density

    diagonal_in = sqrt((width_px / dpi) ** 2 + (height_px / dpi) ** 2)

    '''Clamp to a reasonable range.'''
    diagonal_in = max(4.5, min(diagonal_in, 12))

    return diagonal_in


def adaptive_height(scale, max_height, font_scale):
    """Return a safe adaptive height value that scales with screen size and diagonal."""
    try:
        height = getattr(Window, "height", None)
        '''If height is None or 0 (Window not ready yet), fallback.'''
        if not height or height <= 0:
            return max_height

        return min(height * scale * font_scale, max_height * font_scale)
    except Exception:
        return max_height
