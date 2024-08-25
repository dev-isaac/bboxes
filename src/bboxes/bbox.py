from __future__ import annotations
from enum import Enum
from typing import Literal

from pydantic import NonNegativeFloat, PositiveFloat
from pydantic.dataclasses import dataclass


class OriginType(Enum):
    """
    Enum representing the location of the origin point (0,0) relative to the bounding box.

    Enum values (vertical_type, horizontal_type) are used to
    determine the type of conversion needed (horizontal, vertical, or both)
    when converting from one OriginType to another.
    """

    def __init__(self, v_type: Literal[0, 1], h_type: Literal[0, 1]) -> None:
        self.vertical_type = v_type
        self.horizontal_type = h_type

    TOP_LEFT = (0, 0)
    TOP_RIGHT = (0, 1)
    BOTTOM_LEFT = (1, 0)
    BOTTOM_RIGHT = (1, 1)


@dataclass
class BBox:
    origintype: OriginType
    xmin: NonNegativeFloat
    ymin: NonNegativeFloat
    xmax: NonNegativeFloat
    ymax: NonNegativeFloat

    def __post_init__(self):
        assert (
            self.xmin < self.xmax
        ), f"xmin ({self.xmin}) should not be smaller than xmax ({self.xmax})"
        assert (
            self.ymin < self.ymax
        ), f"ymin ({self.ymin}) should not be smaller than ymax ({self.ymax})"

    @property
    def height(self) -> NonNegativeFloat:
        return self.ymax - self.ymin

    @property
    def width(self) -> NonNegativeFloat:
        return self.xmax - self.xmin

    @property
    def area(self) -> NonNegativeFloat:
        return self.height * self.width

    def convert_origin_type(
        self, to: OriginType, canvas_width: PositiveFloat, canvas_height: PositiveFloat
    ) -> BBox:
        """
        Method to convert a BBox of one OriginType to that of another.
        A new BBox instance is returned.

        Args:
            to (OriginType): destination OriginType
            canvas_width (PositiveFloat):
                Width of the entire "page" in which the bbox is located
            canvas_height (PositiveFloat):
                Height of the entire "page" in which the bbox is located

        Returns:
            BBox: Post-conversion instance of BBox
        """

        x_flip = self.origintype.horizontal_type != to.horizontal_type
        y_flip = self.origintype.vertical_type != to.vertical_type

        if x_flip:
            new_xmin = canvas_width - self.xmax
            new_xmax = canvas_width - self.xmin
        else:
            new_xmin = self.xmin
            new_xmax = self.xmax

        if y_flip:
            new_ymin = canvas_height - self.ymax
            new_ymax = canvas_height - self.ymin
        else:
            new_ymin = self.ymin
            new_ymax = self.ymax

        return BBox(
            origintype=to, xmin=new_xmin, xmax=new_xmax, ymin=new_ymin, ymax=new_ymax
        )
