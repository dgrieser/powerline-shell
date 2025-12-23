import os
import subprocess
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):
    def run(self):
        cmd = self.segment_def["command"]
        self.output = subprocess.check_output(cmd).decode("utf-8").strip()

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
