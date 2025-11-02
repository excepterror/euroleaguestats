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
    if dpi <= 0:
        dpi = 160
    effective_dpi = dpi * (density if density > 0 else 1)
    diagonal_in = sqrt((width_px / effective_dpi) ** 2 + (height_px / effective_dpi) ** 2)
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


def get_screen_dpi():
    """
    Returns the approximate screen DPI (dots per inch).

    - On Android: uses DisplayMetrics (legacy) or WindowMetrics (API >= 30).
    - On desktop platforms: falls back to Kivy's Window.dpi and density.
    """
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
                display_metrics = activity.getResources().getDisplayMetrics()
                xdpi = display_metrics.xdpi
                ydpi = display_metrics.ydpi

            else:
                '''Legacy Android 10 and below.'''
                DisplayMetrics = autoclass('android.util.DisplayMetrics')
                dm = DisplayMetrics()
                display = wm.getDefaultDisplay()
                display.getRealMetrics(dm)

                xdpi = dm.xdpi
                ydpi = dm.ydpi

            '''Average DPI.'''
            if xdpi > 0 and ydpi > 0:
                dpi = (xdpi + ydpi) / 2.0
            elif xdpi > 0:
                dpi = xdpi
            elif ydpi > 0:
                dpi = ydpi
            else:
                dpi = 160.0

            logging.info(f"[ui_helpers.py] Android screen DPI: {dpi:.2f} (xdpi={xdpi:.2f}, ydpi={ydpi:.2f})")
            return round(dpi, 2)

        except Exception as e:
            logging.warning("[ui_helpers.py] get_screen_dpi() failed: %s", e)

    '''Fallback for non-Android platforms.'''
    dpi = getattr(Window, 'dpi', 160)
    density = getattr(Window, 'density', 1)
    if dpi <= 0:
        dpi = 160
    effective_dpi = dpi * (density if density > 0 else 1)
    return round(effective_dpi, 2)


def adaptive_height(scale, max_height, font_scale):
    """
    Adaptive height scaled by screen height and DPI (for consistent physical size).
    """
    try:
        height = get_screen_height_px()

        if not height or height <= 0:
            return max_height

        dpi = get_screen_dpi()

        ref_dpi = 160
        dpi_scale = ref_dpi / dpi if dpi > 0 else 1.0

        value = height * scale * font_scale * dpi_scale
        return min(value, max_height * font_scale)

    except Exception as e:
        logging.warning("[ui_helpers.py] adaptive_height() fallback due to error: %s", e)
        return max_height
