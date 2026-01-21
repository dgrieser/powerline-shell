import os
import shlex
import subprocess
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):
    def run(self):
        cmd = self.segment_def.get("command")
        if not cmd:
            self.output = None
            return
        try:
            if isinstance(cmd, str):
                args = shlex.split(cmd)
            else:
                args = cmd
            self.output = subprocess.check_output(
                args, stderr=subprocess.STDOUT).decode("utf-8").strip()
        except (subprocess.CalledProcessError, OSError, ValueError, TypeError, UnicodeDecodeError):
            self.output = None

    def add_to_powerline(self):
        self.join()
        if self.output:
            self.powerline.append(
                " %s " % self.output,
                self.resolve_color(self.segment_def.get("fg_color", self.powerline.theme.PATH_FG), self.powerline.theme.PATH_FG),
                self.resolve_color(self.segment_def.get("bg_color", self.powerline.theme.PATH_BG), self.powerline.theme.PATH_BG))

    def resolve_color(self, color, fallback):
        if isinstance(color, str) and color.startswith('$'):
            return os.getenv(color[1:].strip('{').strip('}'), fallback)
        return color
