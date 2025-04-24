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
        key_event = autoclass('android.view.KeyEvent')
        if event.getAction() == key_event.ACTION_DOWN and key_code == key_event.KEYCODE_BACK:
            return self.listener()
        return True


class WebViewInModal(ModalView):
    enable_dismiss = BooleanProperty(True)
    webview = ObjectProperty(None)
    layout = ObjectProperty(None)

    def open_web_view(self):
        self.open()

    @run_on_ui_thread
    def on_open(self):
        web_view = autoclass('android.webkit.WebView')
        web_view_client = autoclass('android.webkit.WebViewClient')
        python_activity = autoclass('org.kivy.android.PythonActivity')
        layout_params = autoclass('android.view.ViewGroup$LayoutParams')
        linear_layout = autoclass('android.widget.LinearLayout')
        color = autoclass('android.graphics.Color')

        activity = python_activity.mActivity
        webview = web_view(activity)
        webview.setWebViewClient(web_view_client())
        webview.setBackgroundColor(color.BLACK)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setBuiltInZoomControls(True)
        webview.getSettings().setDisplayZoomControls(False)

        layout = linear_layout(activity)
        layout.setOrientation(linear_layout.VERTICAL)
        layout.addView(webview, layout_params(-1, -1))
        activity.addContentView(layout, layout_params(-1, -1))

        webview.setOnKeyListener(KeyListener(self._back_pressed))
        self.webview = web_view
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
            params.width = self.width
            params.height = self.height
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
            self.webview.clearHistory()
            self.webview.clearCache(True)
            self.webview.clearFormData()
            self.webview.destroy()
            self.webview = None

    def _back_pressed(self):
        if self.webview.canGoBack():
            self.webview.goBack()
        else:
            self.dismiss()
        return True
