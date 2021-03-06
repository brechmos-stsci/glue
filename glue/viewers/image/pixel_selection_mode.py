from __future__ import absolute_import, division, print_function

from glue.core import roi
from glue.config import viewer_tool
from glue.viewers.common.qt.toolbar_mode import ToolbarModeBase
from glue.core.command import ApplySubsetState
from glue.core.subset import SliceSubsetState

__all__ = ['PixelSelectionTool']


@viewer_tool
class PixelSelectionTool(ToolbarModeBase):
    """
    Selects pixel under mouse cursor.
    """

    icon = "glue_point"
    tool_id = 'image:point_selection'
    action_text = 'Pixel'
    tool_tip = 'Select a point based on mouse location'
    status_tip = ('Mouse over to select a point. Click on the image to enable or disable selection.')

    _on_move = False

    def __init__(self, *args, **kwargs):
        super(PixelSelectionTool, self).__init__(*args, **kwargs)
        self._move_callback = self._select_pixel
        self._press_callback = self._on_press

    def _on_press(self, mode):
        self._on_move = not self._on_move

    def _select_pixel(self, mode):
        """
        Select a pixel
        """

        if not self._on_move:
            return

        x, y = self._event_xdata, self._event_ydata

        if x is None or y is None:
            return None

        x = int(round(x))
        y = int(round(y))

        slices = [slice(None)] * self.viewer.state.reference_data.ndim
        slices[self.viewer.state.x_att.axis] = slice(x, x + 1)
        slices[self.viewer.state.y_att.axis] = slice(y, y + 1)

        subset_state = SliceSubsetState(self.viewer.state.reference_data, slices)

        cmd = ApplySubsetState(data_collection=self.viewer._data,
                               subset_state=subset_state,
                               use_current=False)
        self.viewer._session.command_stack.do(cmd)
