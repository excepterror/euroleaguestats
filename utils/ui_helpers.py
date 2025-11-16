from kivy.core.window import Window
from kivy.utils import platform as kivy_platform
from math import sqrt
import logging

# -------------------------------
# ANDROID / CROSS-PLATFORM HELPERS
# -------------------------------

def get_android_display_metrics():
    """
    Returns a dictionary of Android display metrics:
    width_px, height_px, density, density_dpi, xdpi, ydpi.
    Uses WindowMetrics for API >= 30, otherwise Resources.getDisplayMetrics().
    """
    if kivy_platform != "android":
        return None

    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        VERSION = autoclass("android.os.Build$VERSION")

        activity = PythonActivity.mActivity
        wm = activity.getSystemService(Context.WINDOW_SERVICE)
        display_metrics = activity.getResources().getDisplayMetrics()

        if VERSION.SDK_INT >= 30:
            metrics = wm.getCurrentWindowMetrics()
            bounds = metrics.getBounds()
            width_px = bounds.width()
            height_px = bounds.height()
        else:
            width_px = display_metrics.widthPixels
            height_px = display_metrics.heightPixels

        return {
            "width_px": width_px,
            "height_px": height_px,
            "density": display_metrics.density,
            "density_dpi": display_metrics.densityDpi,
            "xdpi": display_metrics.xdpi,
            "ydpi": display_metrics.ydpi,
        }

    except Exception as e:
        logging.warning(f"[ui_helpers] Failed to get Android metrics: {e}")
        return None


# -------------------------------
# SCREEN DIMENSIONS
# -------------------------------

def get_screen_diagonal_in():
    """
    Returns physical screen diagonal in inches.
    Uses modern Android APIs if available, otherwise Kivy Window metrics.
    """
    metrics = get_android_display_metrics()
    if metrics:
        width_in = metrics["width_px"] / metrics["xdpi"]
        height_in = metrics["height_px"] / metrics["ydpi"]
    else:
        width_px, height_px = Window.size
        dpi = getattr(Window, "dpi", 96)
        density = getattr(Window, "density", 1.0)
        dpi *= density if dpi > 0 else 1.0
        width_in = width_px / dpi
        height_in = height_px / dpi

    diagonal_in = sqrt(width_in ** 2 + height_in ** 2)
    return round(diagonal_in, 3)


def get_screen_height_px():
    """
    Returns screen height in pixels.
    Uses Android API if available, otherwise Kivy Window height.
    """
    metrics = get_android_display_metrics()
    if metrics:
        return metrics["height_px"]
    return getattr(Window, "height", 0)


def compute_font_scale(diagonal_in):
    """
    Compute perceptual font scale based on diagonal screen size.
    Nonlinear curve for consistent feel across devices.
    """
    diagonal_in = max(4.5, min(diagonal_in, 12.0))
    exponent = 0.6
    ratio = (diagonal_in / 6.0) ** exponent
    font_scale = max(0.95, min(ratio, 1.3))
    return round(font_scale, 3)


# -------------------------------
# ADAPTIVE HEIGHT
# -------------------------------

def adaptive_height(dp_base, font_scale=1.0, max_dp=None):
    """
    Converts dp_base (logical dp) to px, scaled by font_scale.
    Optional max_dp to clamp size.
    Works for Android and desktop.
    """
    density = getattr(Window, "density", 1.0)

    if kivy_platform == "android":
        metrics = get_android_display_metrics()
        if metrics:
            density = metrics["density"]

    dp_value = dp_base * font_scale
    if max_dp is not None:
        dp_value = min(dp_value, max_dp * font_scale)

    return dp_value * density


# -------------------------------
# DISPLAY INFO / DEBUG PRINT
# -------------------------------

def print_display_metrics_and_size(widget_dp=None):
    """
    Prints cross-platform display metrics and optional widget sizing in px/mm.
    Returns a dictionary of metrics.
    """
    metrics = get_android_display_metrics()
    if metrics:
        width_px = metrics["width_px"]
        height_px = metrics["height_px"]
        density = metrics["density"]
        density_dpi = metrics["density_dpi"]
        xdpi = metrics["xdpi"]
        ydpi = metrics["ydpi"]
    else:
        width_px, height_px = Window.size
        density = getattr(Window, "density", 1.0)
        density_dpi = getattr(Window, "dpi", 96)
        xdpi = ydpi = density_dpi

    diagonal_in = sqrt((width_px / xdpi) ** 2 + (height_px / ydpi) ** 2)
    font_scale = compute_font_scale(diagonal_in)

    if diagonal_in < 6:
        size_class = "PHONE"
    elif diagonal_in < 8:
        size_class = "LARGE PHONE / SMALL TABLET"
    elif diagonal_in < 13:
        size_class = "TABLET / SMALL LAPTOP"
    else:
        size_class = "DESKTOP / LARGE MONITOR"

    print("\n=== DISPLAY METRICS ===")
    print(f"Platform: {kivy_platform}")
    print(f"Resolution: {width_px} × {height_px}")
    print(f"Logical density: {density}")
    print(f"Logical DPI: {density_dpi}")
    print(f"Physical DPI: xdpi={xdpi:.2f}, ydpi={ydpi:.2f}")
    print(f"Screen diagonal: {diagonal_in:.2f}\" ({size_class})")
    print("=======================")

    result = {
        "platform": kivy_platform,
        "width_px": width_px,
        "height_px": height_px,
        "density": density,
        "density_dpi": density_dpi,
        "xdpi": round(xdpi, 2),
        "ydpi": round(ydpi, 2),
        "diag_inches": round(diagonal_in, 2),
        "size_class": size_class,
    }

    if widget_dp is not None:
        px_value = widget_dp * density
        mm_value = (px_value / ydpi) * 25.4

        print(f"Widget logical dp: {widget_dp}")
        print(f"→ Pixels: {px_value:.2f}")
        print(f"→ Physical size: {mm_value:.2f} mm")
        print("=======================")

        result.update({
            "px": round(px_value, 2),
            "mm": round(mm_value, 2),
        })

    return result
