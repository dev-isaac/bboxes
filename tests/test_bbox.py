import pytest
from pydantic_core import ValidationError

from bboxes import BBox, OriginType


@pytest.mark.parametrize(
    argnames=["origin_type"],
    argvalues=[
        pytest.param(OriginType.TOP_LEFT),
        pytest.param(OriginType.BOTTOM_RIGHT),
    ],
)
class TestBBoxInit:
    @pytest.mark.parametrize(
        argnames=["xmin", "ymin", "xmax", "ymax"],
        argvalues=[
            pytest.param(
                -1,
                0,
                1,
                3,
                id="negative min",
            ),
            pytest.param(5, 0, 1, 2, id="xmin greater than xmax"),
            pytest.param(
                0,
                0,
                0,
                0,
                id="origin, zero-area point",
            ),
        ],
    )
    def test_invalid_bbox_init(
        self,
        origin_type: OriginType,
        xmin: float,
        ymin: float,
        xmax: float,
        ymax: float,
    ):
        with pytest.raises(expected_exception=ValidationError):
            BBox(
                origintype=origin_type,
                xmin=xmin,
                ymin=ymin,
                xmax=xmax,
                ymax=ymax,
            )

    @pytest.mark.parametrize(
        argnames=["xmin", "ymin", "xmax", "ymax"],
        argvalues=[
            pytest.param(
                0,
                0,
                1,
                2,
            ),
            pytest.param(
                0.0,
                0.0,
                1.5,
                2.5,
            ),
            pytest.param(
                10.0,
                10.01,
                10.5,
                12.5,
            ),
            pytest.param(
                10,
                10,
                10.01,
                12.5,
            ),
        ],
    )
    def test_bbox_init(
        self,
        origin_type: OriginType,
        xmin: float,
        ymin: float,
        xmax: float,
        ymax: float,
    ):
        BBox(
            origintype=origin_type,
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
        )


@pytest.mark.parametrize(
    argnames="bbox_other",
    argvalues=[
        pytest.param(
            BBox(
                origintype=OriginType.TOP_LEFT,
                xmin=0,
                ymin=0,
                xmax=10,
                ymax=10,
            )
        ),
        pytest.param(
            BBox(
                origintype=OriginType.TOP_LEFT,
                xmin=0,
                ymin=0,
                xmax=10 + 1e-10,
                ymax=10 + 1e-10,
            )
        ),
    ],
)
def test_eq(bbox_other: BBox):
    bbox = BBox(
        origintype=OriginType.TOP_LEFT,
        xmin=0,
        ymin=0,
        xmax=10,
        ymax=10,
    )

    assert bbox == bbox_other


@pytest.mark.parametrize(
    argnames="bbox_other",
    argvalues=[
        pytest.param(
            BBox(
                origintype=OriginType.BOTTOM_RIGHT,
                xmin=0,
                ymin=0,
                xmax=10,
                ymax=10,
            )
        ),
        pytest.param(
            BBox(
                origintype=OriginType.TOP_LEFT,
                xmin=0,
                ymin=0,
                xmax=10 + 1e-10,
                ymax=11,
            )
        ),
    ],
)
def test_not_eq(bbox_other: BBox):
    bbox = BBox(
        origintype=OriginType.TOP_LEFT,
        xmin=0,
        ymin=0,
        xmax=10,
        ymax=10,
    )
    assert bbox != bbox_other

