# main.py

import sys
import ctypes

from PySide6.QtWidgets import QApplication
from zebra.zebra_menu import ZebraMenu

from pathlib import Path
import glfw
from OpenGL import GL as gl
import time
from graphics.graphics_app_shell import GraphicsAppShell
from graphics.graphics_pipeline import GraphicsPipeline
from graphics.graphics_library import GraphicsLibrary

from pong.pong_asset_bundle import PongAssetBundle
from pong.pong_scene import PongScene

from heart.heart_asset_bundle import HeartAssetBundle
from heart.heart_scene import HeartScene


def framebuffer_size_callback(window, width, height):
    app_shell = glfw.get_window_user_pointer(window)
    if app_shell:
        screen_width, screen_height = glfw.get_window_size(window)
        screen_scale_x, screen_scale_y = glfw.get_window_content_scale(window)
        frame_buffer_width, frame_buffer_height = glfw.get_framebuffer_size(window)
        if app_shell.scene:
            scene = app_shell.scene
            if scene.graphics:
                graphics = scene.graphics
                graphics.resize(screen_width=screen_width,
                                screen_height=screen_height,
                                screen_scale_x=screen_scale_x,
                                screen_scale_y=screen_scale_y,
                                frame_buffer_width=frame_buffer_width,
                                frame_buffer_height=frame_buffer_height)
        app_shell.resize()

def key_callback(window, key, scancode, action, mods):
    mod_control = bool(mods & (glfw.MOD_CONTROL | glfw.MOD_SUPER))
    mod_shift = bool(mods & glfw.MOD_SHIFT)
    mod_alt = bool(mods & glfw.MOD_ALT)
    app_shell = glfw.get_window_user_pointer(window)
    if app_shell:
        if action == glfw.PRESS:
            app_shell.key_down(
                key=key,
                mod_control=mod_control,
                mod_alt=mod_alt,
                mod_shift=mod_shift,
            )
        elif action == glfw.RELEASE:
            app_shell.key_up(
                key=key,
                mod_control=mod_control,
                mod_alt=mod_alt,
                mod_shift=mod_shift,
            )

    if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
def mouse_button_callback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT:
        mapped_button = -1
    elif button == glfw.MOUSE_BUTTON_MIDDLE:
        mapped_button = 0
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        mapped_button = 1
    else:
        mapped_button = None  # unknown or extra buttons
    
    xpos, ypos = glfw.get_cursor_pos(window)
    app_shell = glfw.get_window_user_pointer(window)
    if app_shell and mapped_button is not None:
        if app_shell.scene:
            if app_shell.scene.graphics:
                xpos *= app_shell.scene.graphics.screen_scale_x
                ypos *= app_shell.scene.graphics.screen_scale_y
        if action == glfw.PRESS:
            app_shell.mouse_down(
                button=mapped_button,
                xpos=xpos,
                ypos=ypos,
            )
        elif action == glfw.RELEASE:
            app_shell.mouse_up(
                button=mapped_button,
                xpos=xpos,
                ypos=ypos,
            )

def cursor_pos_callback(window, xpos, ypos):
    app_shell = glfw.get_window_user_pointer(window)
    if app_shell:
        if app_shell.scene:
            if app_shell.scene.graphics:
                xpos *= app_shell.scene.graphics.screen_scale_x
                ypos *= app_shell.scene.graphics.screen_scale_y
        app_shell.mouse_move(xpos=xpos, ypos=ypos)

def scroll_callback(window, xoffset, yoffset):
    direction = 0
    if yoffset > 0:
        direction = -1
    elif yoffset < 0:
        direction = 1
    app_shell = glfw.get_window_user_pointer(window)
    if app_shell:
        app_shell.mouse_wheel(direction=direction)
    
def main():

    if not glfw.init():
        print("Failed to initialize GLFW")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    width, height = 1280, 960
    window = glfw.create_window(width, height, "(  .  Y  .  )", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)

    screen_width, screen_height = glfw.get_window_size(window)
    screen_scale_x, screen_scale_y = glfw.get_window_content_scale(window)
    frame_buffer_width, frame_buffer_height = glfw.get_framebuffer_size(window)
    
    base_dir = Path(__file__).resolve().parent
    pipeline = GraphicsPipeline()
    graphics = GraphicsLibrary(screen_width=screen_width,
                               screen_height=screen_height,
                               screen_scale_x=screen_scale_x,
                               screen_scale_y=screen_scale_y,
                               frame_buffer_width=frame_buffer_width,
                               frame_buffer_height=frame_buffer_height)
    
    # assets = PongAssetBundle()
    # pong_scene = LabelingScene(graphics=graphics, pipeline=pipeline, assets=assets)
    # pong_scene = PongScene(graphics=graphics, pipeline=pipeline, assets=assets)
    # app_shell = GraphicsAppShell(scene=pong_scene)

    assets = HeartAssetBundle()
    heart_scene = HeartScene(graphics, pipeline, assets)
    app_shell = GraphicsAppShell(heart_scene)

    glfw.set_window_user_pointer(window, app_shell)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # The Keyboard
    glfw.set_key_callback(window, key_callback)

    # The Mouse
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    app_shell.wake()

    assets.load(graphics=graphics)
    app_shell.prepare()

    # inside main(), after creating the GLFW window:
    qt_app = QApplication.instance() or QApplication([])
    zebra_menu = ZebraMenu(is_draggable=True)
    zebra_menu.show()

    # optional: hook signals
    zebra_menu.zebra.threshold_changed.connect(lambda v: print("threshold", v))
    zebra_menu.zebra.knockout_changed.connect(lambda v: print("knockout", v))
    zebra_menu.zebra.bw_changed.connect(lambda b: print("bw", b))
    zebra_menu.zebra.next_image_clicked.connect(lambda: print("next image"))
    zebra_menu.zebra.previous_image_clicked.connect(lambda: print("previous image"))
    zebra_menu.zebra.calibrate_clicked.connect(lambda: print("calibrate"))
    zebra_menu.zebra.reset_clicked.connect(lambda: print("reset"))



    previous_time = time.time()
    while not glfw.window_should_close(window):
        current_time = time.time()
        dt = current_time - previous_time
        dt = min(dt, 0.1)
        previous_time = current_time
        app_shell.update(dt)
        app_shell.draw()
        glfw.swap_buffers(window)

        qt_app.processEvents()

        glfw.poll_events()

    app_shell.dispose()
    assets.dispose()
    glfw.terminate()
    sys.exit(0)

if __name__ == "__main__":
    main()
