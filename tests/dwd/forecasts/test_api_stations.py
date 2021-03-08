# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from wetterdienst.dwd.forecasts import DwdMosmixRequest, DwdMosmixType
from wetterdienst.metadata.columns import Columns


@pytest.mark.remote
def test_dwd_mosmix_stations_success():
    # Existing combination of parameters
    request = DwdMosmixRequest(mosmix_type=DwdMosmixType.LARGE)

    df = request.all().df

    assert not df.empty

    # TODO: fix empty state value to be pd.NA

    assert_frame_equal(
        df.loc[df[Columns.STATION_ID.value] == "01001", :].reset_index(drop=True),
        pd.DataFrame(
            {
                "STATION_ID": ["01001"],
                "ICAO_ID": ["ENJA"],
                "FROM_DATE": pd.to_datetime([pd.NA], utc=True),
                "TO_DATE": pd.to_datetime([pd.NaT], utc=True),
                "HEIGHT": [10.0],
                "LATITUDE": [70.93],
                "LONGITUDE": [-8.0],
                "STATION_NAME": ["JAN MAYEN"],
                "STATE": ["nan"],
            }
        ),
    )