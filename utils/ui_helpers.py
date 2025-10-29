from kivy.core.window import Window
from math import sqrt
from kivy.utils import platform as kivy_platform

import logging

def get_screen_diagonal_in():
    """
    Returns the physical screen diagonal in inches.
    Uses WindowManager.getCurrentWindowMetrics() for API >= 30,
    and Display.getRealMetrics() for older Android versions.
    Falls back to Kivy Window metrics on other platforms.
    """
    from kivy.core.window import Window

    if kivy_platform == 'android':
        try:
            from jnius import autoclass

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            VERSION = autoclass('android.os.Build$VERSION')

            activity = PythonActivity.mActivity
            window_manager = activity.getSystemService(Context.WINDOW_SERVICE)

            if VERSION.SDK_INT >= 30:
                '''Android 11+ modern method.'''
                metrics = window_manager.getCurrentWindowMetrics()
                bounds = metrics.getBounds()

                width_px = bounds.width()
                height_px = bounds.height()

                display_metrics = activity.getResources().getDisplayMetrics()
                xdpi = display_metrics.xdpi
                ydpi = display_metrics.ydpi

                logging.info(f"[ui_helpers.py] [API>=30] width={width_px}, height={height_px}, xdpi={xdpi}, ydpi={ydpi}")

            else:
                '''Legacy Android 10 and below.'''
                DisplayMetrics = autoclass('android.util.DisplayMetrics')
                display_metrics = DisplayMetrics()
                display = window_manager.getDefaultDisplay()
                display.getRealMetrics(display_metrics)

                width_px = display_metrics.widthPixels
                height_px = display_metrics.heightPixels
                xdpi = display_metrics.xdpi
                ydpi = display_metrics.ydpi

                logging.info(f"[ui_helpers.py] [Legacy API] width={width_px}, height={height_px}, xdpi={xdpi}, ydpi={ydpi}")

            '''Compute physical diagonal.'''
            diagonal_in = sqrt((width_px / xdpi) ** 2 + (height_px / ydpi) ** 2)
            return round(diagonal_in, 3)

        except Exception as e:
            print("Android API metrics failed:", e)

    '''Fallback for non-Android platforms.'''
    width_px, height_px = Window.size
    dpi = getattr(Window, 'dpi', 160)
    density = getattr(Window, 'density', 1)
    dpi = dpi * density if dpi > 0 else 160
    diagonal_in = sqrt((width_px / dpi) ** 2 + (height_px / dpi) ** 2)
    return round(diagonal_in, 3)


def compute_font_scale(diagonal_in):
    """
    Compute a perceptually smoother font scale from screen diagonal.
    Nonlinear curve: gentle scaling that feels consistent across devices.
    """
    '''Clamp to reasonable device range.'''
    diagonal_in = max(4.5, min(diagonal_in, 12.0))

    '''Nonlinear ease-out curve.'''
    exponent = 0.6
    ratio = (diagonal_in / 6.0) ** exponent

    '''Keep in sensible bounds.'''
    font_scale = max(0.95, min(ratio, 1.3))
    return round(font_scale, 3)


def get_screen_height_px():
    """Return the screen height in pixels, using Android API if available."""
    if kivy_platform == 'android':
        try:
            from jnius import autoclass

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            VERSION = autoclass('android.os.Build$VERSION')

            activity = PythonActivity.mActivity
            wm = activity.getSystemService(Context.WINDOW_SERVICE)

            '''Modern method for Android 11+ (API 30+).'''
            if VERSION.SDK_INT >= 30:
                metrics = wm.getCurrentWindowMetrics()
                bounds = metrics.getBounds()
                return bounds.height()
            else:
                '''Legacy method for older Android versions.'''
                DisplayMetrics = autoclass('android.util.DisplayMetrics')
                dm = DisplayMetrics()
                wm.getDefaultDisplay().getRealMetrics(dm)
                return dm.heightPixels
        except Exception as e:
            logging.warning("[ui_helpers.py] Failed to get Android screen height:", e)

    '''Fallback for desktop.'''
    return getattr(Window, "height", 0)


def adaptive_height(scale, max_height, font_scale):
    """
    Return a safe adaptive height value that scales with screen size and diagonal.
    Uses Android APIs for accurate height on real devices.
    """
    try:
        height = get_screen_height_px()

        '''Handle case where Window or metrics not ready yet.'''
        if not height or height <= 0:
            return max_height

        '''Apply scaling.'''
        value = height * scale * font_scale

        '''Clamp to avoid absurdly large values.'''
        return min(value, max_height * font_scale)

    except Exception as e:
        logging.warning("[ui_helpers.py] adaptive_height() fallback due to error:", e)
        return max_height
