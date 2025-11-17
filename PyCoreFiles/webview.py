import logging

from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty, ObjectProperty
from android.runnable import run_on_ui_thread
from jnius import autoclass, cast, PythonJavaClass, java_method

logging.getLogger().setLevel(logging.INFO)


class KeyListener(PythonJavaClass):
    __javacontext__ = 'app'
    __javainterfaces__ = ['android/view/View$OnKeyListener']

    def __init__(self, listener):
        super().__init__()
        self.listener = listener

    @java_method('(Landroid/view/View;ILandroid/view/KeyEvent;)Z')
    def onKey(self, v, key_code, event):
        KeyEvent = autoclass('android.view.KeyEvent')
        # Only on ACTION_DOWN and BACK key do our custom action
        if event.getAction() == KeyEvent.ACTION_DOWN and key_code == KeyEvent.KEYCODE_BACK:
            return self.listener()
        # Return False to allow propagation when not handled (optional)
        return False


class WebViewInModal(ModalView):
    enable_dismiss = BooleanProperty(True)
    webview = ObjectProperty(None)
    layout = ObjectProperty(None)

    # Keep strong references here
    _key_listener = None

    def open_web_view(self):
        self.open()

    @run_on_ui_thread
    def on_open(self):
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        LinearLayout = autoclass('android.widget.LinearLayout')
        Color = autoclass('android.graphics.Color')

        activity = PythonActivity.mActivity
        webview = WebView(activity)
        webview.setWebViewClient(WebViewClient())
        webview.setBackgroundColor(Color.BLACK)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setBuiltInZoomControls(True)
        webview.getSettings().setDisplayZoomControls(False)

        layout = LinearLayout(activity)
        layout.setOrientation(LinearLayout.VERTICAL)
        layout.addView(webview, LayoutParams(-1, -1))
        activity.addContentView(layout, LayoutParams(-1, -1))

        # keep a strong reference to the listener to avoid GC + crash
        self._key_listener = KeyListener(self._back_pressed)
        webview.setOnKeyListener(self._key_listener)

        # assign the instance (not the autoclass)
        self.webview = webview
        self.layout = layout

        try:
            webview.loadUrl('https://github.com/excepterror/euroleaguestats/blob/master/PRIVACY%20POLICY.md')
        except Exception as e:
            logging.warning('Webview.on_open(): {}'.format(str(e)))
            self.dismiss()

    @run_on_ui_thread
    def on_size(self, instance, size):
        if self.webview:
            params = self.webview.getLayoutParams()
            params.width = int(self.width)
            params.height = int(self.height)
            self.webview.setLayoutParams(params)

    def pause(self):
        if self.webview:
            self.webview.pauseTimers()
            self.webview.onPause()

    def resume(self):
        if self.webview:
            self.webview.onResume()
            self.webview.resumeTimers()

    @run_on_ui_thread
    def on_dismiss(self):
        view_group = autoclass('android.view.ViewGroup')
        if self.enable_dismiss:
            self.enable_dismiss = False
            parent = cast(view_group, self.layout.getParent())
            if parent is not None:
                parent.removeView(self.layout)

            # cleanup listener (unset) and webview properly
            if self.webview:
                try:
                    # Remove listener to avoid further Java callbacks
                    self.webview.setOnKeyListener(None)
                except Exception:
                    pass
                try:
                    self.webview.clearHistory()
                    self.webview.clearCache(True)
                    self.webview.clearFormData()
                    self.webview.destroy()
                except Exception:
                    pass
                finally:
                    self.webview = None

            # drop our strong reference
            self._key_listener = None

    def _back_pressed(self):
        if self.webview and self.webview.canGoBack():
            self.webview.goBack()
        else:
            self.dismiss()
        return True
