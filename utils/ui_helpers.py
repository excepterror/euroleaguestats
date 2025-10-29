from kivy.core.window import Window
from math import sqrt
from kivy.utils import platform as kivy_platform

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
                # Android 11+ modern method
                metrics = window_manager.getCurrentWindowMetrics()
                bounds = metrics.getBounds()

                width_px = bounds.width()
                height_px = bounds.height()

                display_metrics = activity.getResources().getDisplayMetrics()
                xdpi = display_metrics.xdpi
                ydpi = display_metrics.ydpi

                print(f"[API>=30] width={width_px}, height={height_px}, xdpi={xdpi}, ydpi={ydpi}")

            else:
                # Legacy Android 10 and below
                DisplayMetrics = autoclass('android.util.DisplayMetrics')
                display_metrics = DisplayMetrics()
                display = window_manager.getDefaultDisplay()
                display.getRealMetrics(display_metrics)

                width_px = display_metrics.widthPixels
                height_px = display_metrics.heightPixels
                xdpi = display_metrics.xdpi
                ydpi = display_metrics.ydpi

                print(f"[Legacy API] width={width_px}, height={height_px}, xdpi={xdpi}, ydpi={ydpi}")

            # Compute physical diagonal
            diagonal_in = sqrt((width_px / xdpi) ** 2 + (height_px / ydpi) ** 2)
            return round(diagonal_in, 3)

        except Exception as e:
            print("Android API metrics failed:", e)

    # Fallback for non-Android platforms
    width_px, height_px = Window.size
    dpi = getattr(Window, 'dpi', 160)
    density = getattr(Window, 'density', 1)
    dpi = dpi * density if dpi > 0 else 160
    diagonal_in = sqrt((width_px / dpi) ** 2 + (height_px / dpi) ** 2)
    return round(diagonal_in, 3)


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
