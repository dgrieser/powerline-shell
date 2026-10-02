"""Virtualenv segment with configurable colors.

Shows the virtualenv or conda environment, with ".venv" meaning the name of
its parent directory. ``fg_color`` and ``bg_color`` of the segment definition
in config.json override the theme colors. Values starting with ``$`` are
resolved from the environment, so the palette can be kept in e.g. ~/.colorrc
alongside the other POWERLINE_* colors.

Colors may use the ``.colorrc`` convention of appending attributes to the color
number, e.g. ``221:bold`` or ``221:bold:italic``. powerline-shell itself only
understands a bare number, so the attributes are emitted as their own escape
sequences around the segment text and switched off again at its end.
"""

import os

from ..utils import BasicSegment

# attribute name -> (SGR code to enable, SGR code to disable)
ATTRIBUTES = {
    "bold": (1, 22),
    "dim": (2, 22),
    "italic": (3, 23),
    "underline": (4, 24),
    "blink": (5, 25),
    "reverse": (7, 27),
    "strike": (9, 29),
}


class Segment(BasicSegment):
    def add_to_powerline(self):
        env = os.getenv('VIRTUAL_ENV') \
            or os.getenv('CONDA_ENV_PATH') \
            or os.getenv('CONDA_DEFAULT_ENV')
        if os.getenv('VIRTUAL_ENV') \
            and os.path.basename(env) == '.venv':
            env = os.path.basename(os.path.dirname(env))
        if not env:
            return
        env_name = os.path.basename(env)
        bg, _ = self.split_attributes(self.resolve_color(
            self.segment_def.get("bg_color", self.powerline.theme.VIRTUAL_ENV_BG),
            self.powerline.theme.VIRTUAL_ENV_BG,
        ))
        fg, attributes = self.split_attributes(self.resolve_color(
            self.segment_def.get("fg_color", self.powerline.theme.VIRTUAL_ENV_FG),
            self.powerline.theme.VIRTUAL_ENV_FG,
        ))
        on = ''.join(self.sgr(ATTRIBUTES[a][0]) for a in attributes)
        off = ''.join(self.sgr(ATTRIBUTES[a][1]) for a in reversed(attributes))
        self.powerline.append(on + " " + env_name + " " + off, fg, bg)

    def resolve_color(self, color, fallback):
        if isinstance(color, str) and color.startswith('$'):
            return os.getenv(color[1:].strip('{').strip('}'), fallback)
        return color

    def split_attributes(self, color):
        """Split "221:bold" into the color 221 and the attributes to apply."""
        if not isinstance(color, str) or ':' not in color:
            return color, []
        parts = color.split(':')
        return parts[0], [p for p in parts[1:] if p in ATTRIBUTES]

    def sgr(self, code):
        return self.powerline.color_template % ('[%dm' % code)
