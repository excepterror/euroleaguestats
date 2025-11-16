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


def adaptive_height(dp_base, font_scale=1.0, max_dp=None):
    """
    dp_base: base button height in dp (e.g. 50)
    font_scale: your nonlinear diagonal-based scale
    max_dp: optional upper limit in dp

    Returns px value.
    """
    from kivy.core.window import Window
    density = getattr(Window, "density", 1)

    '''Apply font scale.'''
    dp_value = dp_base * font_scale

    '''Optional clamp.'''
    if max_dp is not None:
        dp_value = min(dp_value, max_dp * font_scale)

    '''Convert dp to px.'''
    return dp_value * density


def print_display_metrics_and_size(widget_dp=None):
    """
    Cross-platform metrics (Android + Windows + macOS + Linux)
    Converts a widget's logical dp size to:
        - px (pixels)
        - mm (physical size)
        - confirmed dp
    Uses modern Android API on SDK 30+ (getCurrentWindowMetrics)
    """

    from kivy.core.window import Window
    from kivy.utils import platform as kivy_platform

    PLATFORM = kivy_platform
    is_android = PLATFORM == "android"

    diagonal_in = get_screen_diagonal_in()
    font_scale = compute_font_scale(diagonal_in)

    '''-----------------------------
             ANDROID SECTION
      -----------------------------'''
    if is_android:
        try:
            from jnius import autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")
            VERSION = autoclass("android.os.Build$VERSION")
            DisplayMetrics = autoclass("android.util.DisplayMetrics")

            activity = PythonActivity.mActivity
            wm = activity.getSystemService(Context.WINDOW_SERVICE)

            '''-----------------------------
                      Modern API >=30
               -----------------------------'''
            if VERSION.SDK_INT >= 30:
                metrics_obj = wm.getCurrentWindowMetrics()
                bounds = metrics_obj.getBounds()
                width_px = bounds.width()
                height_px = bounds.height()
                '''Physical DPI.'''
                display_metrics = activity.getResources().getDisplayMetrics()
                xdpi = float(display_metrics.xdpi)
                ydpi = float(display_metrics.ydpi)
                density = display_metrics.density
                density_dpi = display_metrics.densityDpi
            else:
                # Legacy API <30
                metrics = DisplayMetrics()
                display = wm.getDefaultDisplay()
                display.getRealMetrics(metrics)
                width_px = metrics.widthPixels
                height_px = metrics.heightPixels
                xdpi = float(metrics.xdpi)
                ydpi = float(metrics.ydpi)
                density = metrics.density
                density_dpi = metrics.densityDpi

        except Exception as e:
            print("ANDROID ERROR:", e)
            is_android = False

    '''-----------------------------
              DESKTOP SECTION
       -----------------------------'''
    if not is_android:
        width_px, height_px = Window.size
        density = getattr(Window, "density", 1.0)
        density_dpi = getattr(Window, "dpi", 96)
        xdpi = density_dpi
        ydpi = density_dpi

    '''-----------------------------
            Physical screen size
       -----------------------------'''
    width_in = width_px / xdpi
    height_in = height_px / ydpi
    diagonal_in = (width_in**2 + height_in**2) ** 0.5

    '''Device classification.'''
    if diagonal_in < 6:
        size_class = "PHONE"
    elif diagonal_in < 8:
        size_class = "LARGE PHONE / SMALL TABLET"
    elif diagonal_in < 13:
        size_class = "TABLET / SMALL LAPTOP"
    else:
        size_class = "DESKTOP / LARGE MONITOR"

    '''-----------------------------
             Print device info
       -----------------------------'''
    print("\n=== DISPLAY METRICS ===")
    print(f"Platform: {PLATFORM}")
    print(f"Resolution: {width_px} × {height_px}")
    print(f"Logical density: {density}")
    print(f"Logical DPI: {density_dpi}")
    print(f"Physical DPI: xdpi={xdpi:.2f}, ydpi={ydpi:.2f}")
    print(f"Screen diagonal: {diagonal_in:.2f}\"  ({size_class})")
    print("=======================")

    result = {
        "platform": PLATFORM,
        "width_px": width_px,
        "height_px": height_px,
        "density": density,
        "density_dpi": density_dpi,
        "xdpi": round(xdpi, 2),
        "ydpi": round(ydpi, 2),
        "diag_inches": round(diagonal_in, 2),
        "size_class": size_class,
    }

    '''-------------------------------
       Convert widget dp to px and mm
       -------------------------------'''
    if widget_dp is not None:
        px_value = widget_dp * density  # dp → pixels
        mm_value = (px_value / ydpi) * 25.4  # pixels → mm
        dp_value = widget_dp * font_scale  # verify dp

        print(f"Widget logical dp: {widget_dp}")
        print(f"→ Pixels: {px_value:.2f}")
        print(f"→ Physical size: {mm_value:.2f} mm")
        print(f"→ Confirmed dp: {dp_value:.2f}")
        print("=======================")

        result.update({
            "dp": round(dp_value, 2),
            "px": round(px_value, 2),
            "mm": round(mm_value, 2),
        })

    return result
