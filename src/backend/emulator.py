import io
import time
from PIL import Image

from desmume.controls import Keys, keymask
from desmume.emulator import DeSmuME, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_PIXEL_SIZE


class GBA(object):
    KEY_B = 0
    KEY_A = 1
    KEY_SELECT = 2
    KEY_START = 3
    KEY_RIGHT = 4
    KEY_LEFT = 5
    KEY_UP = 6
    KEY_DOWN = 7
    KEY_R = 8
    KEY_L = 9


KEYMAP = {
    GBA.KEY_A: Keys.KEY_A,
    GBA.KEY_B: Keys.KEY_B,
    GBA.KEY_SELECT: Keys.KEY_SELECT,
    GBA.KEY_START: Keys.KEY_START,
    GBA.KEY_RIGHT: Keys.KEY_RIGHT,
    GBA.KEY_LEFT: Keys.KEY_LEFT,
    GBA.KEY_UP: Keys.KEY_UP,
    GBA.KEY_DOWN: Keys.KEY_DOWN,
    GBA.KEY_R: Keys.KEY_R,
    GBA.KEY_L: Keys.KEY_L
}

class Emulator(object):
    def __init__(self, web_server):
        self.web_server = web_server
        self.enabled = False
        self.paused = False

        self.fps = 480
        self.core = None
        self.image = None
        self.imageBuf = io.BytesIO()

        self.turbo = False
        self.turbo_value = 2

        self.keys_down = []

    def init_with_path(self, path):
        if self.core is None:
            self.core = DeSmuME()
        else:
            try:
                self.core.close()
            except Exception:
                pass
        self.core.open(path)

        if hasattr(self.core, 'volume_set'):
            self.core.volume_set(0)

        self.core.reset()

        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT * 2
        self.web_server.set_size(width, height)
        self.enabled = True

    def save_state(self, slot):
        if not self.core:
            return
        self.core.savestate.save(slot)

    def load_state(self, slot):
        if not self.core:
            return
        self.core.savestate.load(slot)

    def stop(self):
        self.enabled = False

    def run(self, path):
        self.init_with_path(path)
        print('[!] Emulator started')
        last_frame = time.time()
        last_display_frame = time.time()
        try:
            while self.enabled:
                if self.paused:
                    time.sleep(1)
                    continue
                curr_frame = time.time()
                delta = curr_frame - last_frame

                multi = self.turbo_value if self.turbo else 1
                framecap = multi * 60
                if delta < 1 / framecap:
                    continue
                last_frame = curr_frame

                self.core.cycle(False)

                display_delta = curr_frame - last_display_frame
                if display_delta >= 1 / self.fps:
                    self.web_server.emit_frame(self.get_frame())
                    last_display_frame = curr_frame
        except Exception as e:
            print(e)
        finally:
            self.release_core()

    def set_turbo(self, enabled):
        self.turbo = enabled

    def set_turbo_value(self, multi):
        self.turbo_value = multi

    def set_fps(self, fps):
        self.fps = fps

    def get_frame(self):
        try:
            self.imageBuf.truncate(0)
            self.imageBuf.seek(0)
            framebuffer = bytes(self.core.display_buffer_as_rgbx())
            upper = Image.frombytes(
                'RGB',
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                framebuffer[:SCREEN_PIXEL_SIZE * 4],
                'raw',
                'BGRX'
            )
            lower = Image.frombytes(
                'RGB',
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                framebuffer[SCREEN_PIXEL_SIZE * 4:SCREEN_PIXEL_SIZE * 8],
                'raw',
                'BGRX'
            )
            image = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
            image.paste(upper, (0, 0))
            image.paste(lower, (0, SCREEN_HEIGHT))
            image.save(
                self.imageBuf,
                format="WebP",
                quality=70,
                method=0
            )
            return self.imageBuf.getvalue()[:]
        except Exception as e:
            print("[!!] Error converting frame: {}".format(e))
            return []

    def check_directional(self, key):
        directional_keys = [GBA.KEY_RIGHT, GBA.KEY_UP, GBA.KEY_DOWN, GBA.KEY_LEFT]

        if key not in directional_keys:
            return

        for dkey in directional_keys:
            if dkey != key and dkey in self.keys_down:
                self.key_up(dkey)

    def key_down(self, key):
        self.check_directional(key)
        if key not in self.keys_down:
            self.keys_down.append(key)
            if key in KEYMAP:
                self.core.input.keypad_add_key(keymask(KEYMAP[key]))

    def key_up(self, key):
        if key in self.keys_down:
            self.keys_down.remove(key)
            if key in KEYMAP:
                self.core.input.keypad_rm_key(keymask(KEYMAP[key]))

    def release_keys(self):
        for key in self.keys_down[:]:
            self.key_up(key)

    def release_core(self):
        if not self.core:
            return
        try:
            self.release_keys()
        except Exception:
            pass
        try:
            self.core.close()
        except Exception:
            pass

import io
import time
from PIL import Image

from desmume.controls import Keys, keymask
from desmume.emulator import DeSmuME, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_PIXEL_SIZE


class GBA(object):
    KEY_B = 0
    KEY_A = 1
    KEY_SELECT = 2
    KEY_START = 3
    KEY_RIGHT = 4
    KEY_LEFT = 5
    KEY_UP = 6
    KEY_DOWN = 7
    KEY_R = 8
    KEY_L = 9


KEYMAP = {
    GBA.KEY_A: Keys.KEY_A,
    GBA.KEY_B: Keys.KEY_B,
    GBA.KEY_SELECT: Keys.KEY_SELECT,
    GBA.KEY_START: Keys.KEY_START,
    GBA.KEY_RIGHT: Keys.KEY_RIGHT,
    GBA.KEY_LEFT: Keys.KEY_LEFT,
    GBA.KEY_UP: Keys.KEY_UP,
    GBA.KEY_DOWN: Keys.KEY_DOWN,
    GBA.KEY_R: Keys.KEY_R,
    GBA.KEY_L: Keys.KEY_L
}

class Emulator(object):
    def __init__(self, web_server):
        self.web_server = web_server
        self.enabled = False
        self.paused = False

        self.fps = 480
        self.core = None
        self.image = None
        self.imageBuf = io.BytesIO()

        self.turbo = False
        self.turbo_value = 2

        self.keys_down = []

    def init_with_path(self, path):
        if self.core is None:
            self.core = DeSmuME()
        else:
            try:
                self.core.close()
            except Exception:
                pass
        self.core.open(path)

        if hasattr(self.core, 'volume_set'):
            self.core.volume_set(0)

        self.core.reset()

        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT * 2
        self.web_server.set_size(width, height)
        self.enabled = True

    def save_state(self, slot):
        if not self.core:
            return
        self.core.savestate.save(slot)

    def load_state(self, slot):
        if not self.core:
            return
        self.core.savestate.load(slot)

    def stop(self):
        self.enabled = False

    def run(self, path):
        self.init_with_path(path)
        print('[!] Emulator started')
        last_frame = time.time()
        last_display_frame = time.time()
        try:
            while self.enabled:
                if self.paused:
                    time.sleep(1)
                    continue
                curr_frame = time.time()
                delta = curr_frame - last_frame

                multi = self.turbo_value if self.turbo else 1
                framecap = multi * 60
                if delta < 1 / framecap:
                    continue
                last_frame = curr_frame

                self.core.cycle(False)

                display_delta = curr_frame - last_display_frame
                if display_delta >= 1 / self.fps:
                    self.web_server.emit_frame(self.get_frame())
                    last_display_frame = curr_frame
        except Exception as e:
            print(e)
        finally:
            self.release_core()

    def set_turbo(self, enabled):
        self.turbo = enabled

    def set_turbo_value(self, multi):
        self.turbo_value = multi

    def set_fps(self, fps):
        self.fps = fps

    def get_frame(self):
        try:
            self.imageBuf.truncate(0)
            self.imageBuf.seek(0)
            framebuffer = bytes(self.core.display_buffer_as_rgbx())
            upper = Image.frombytes(
                'RGB',
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                framebuffer[:SCREEN_PIXEL_SIZE * 4],
                'raw',
                'BGRX'
            )
            lower = Image.frombytes(
                'RGB',
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                framebuffer[SCREEN_PIXEL_SIZE * 4:SCREEN_PIXEL_SIZE * 8],
                'raw',
                'BGRX'
            )
            image = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
            image.paste(upper, (0, 0))
            image.paste(lower, (0, SCREEN_HEIGHT))
            image.save(
                self.imageBuf,
                format="WebP",
                quality=70,
                method=0
            )
            return self.imageBuf.getvalue()[:]
        except Exception as e:
            print("[!!] Error converting frame: {}".format(e))
            return []

    def check_directional(self, key):
        directional_keys = [GBA.KEY_RIGHT, GBA.KEY_UP, GBA.KEY_DOWN, GBA.KEY_LEFT]

        if key not in directional_keys:
            return

        for dkey in directional_keys:
            if dkey != key and dkey in self.keys_down:
                self.key_up(dkey)

    def key_down(self, key):
        self.check_directional(key)
        if key not in self.keys_down:
            self.keys_down.append(key)
            if key in KEYMAP:
                self.core.input.keypad_add_key(keymask(KEYMAP[key]))

    def key_up(self, key):
        if key in self.keys_down:
            self.keys_down.remove(key)
            if key in KEYMAP:
                self.core.input.keypad_rm_key(keymask(KEYMAP[key]))

    def release_keys(self):
        for key in self.keys_down[:]:
            self.key_up(key)

    def release_core(self):
        if not self.core:
            return
        try:
            self.release_keys()
        except Exception:
            pass
        try:
            self.core.close()
        except Exception:
            pass
