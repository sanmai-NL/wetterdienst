.. python-examples:

Python Examples
###############

DWD
****

Observation
===========

Get available parameters for daily historical data of DWD:

.. ipython:: python
    :okwarning:

    from wetterdienst import Resolution, Period
    from wetterdienst.provider.dwd.observation import DwdObservationRequest

    observations_meta = DwdObservationRequest.discover(
        resolution=Resolution.DAILY,
    )

    # Available parameter sets
    print(observations_meta)

    # Available individual parameters
    observations_meta = DwdObservationRequest.discover(
        resolution=Resolution.DAILY, flatten=False
    )

    print(observations_meta)

Get stations for daily historical precipitation:

.. ipython:: python
    :okwarning:

    from wetterdienst import Resolution, Period
    from wetterdienst.provider.dwd.observation import DwdObservationDataset

    stations = DwdObservationRequest(
        parameter=DwdObservationDataset.PRECIPITATION_MORE,
        resolution=Resolution.DAILY,
        period=Period.HISTORICAL
    )

    print(stations.all().df.head())

Get data for a dataset:

.. ipython:: python
    :okwarning:

    from wetterdienst import Resolution, Period
    from wetterdienst.provider.dwd.observation import DwdObservationDataset

    stations = DwdObservationRequest(
        parameter=DwdObservationDataset.PRECIPITATION_MORE,
        resolution=Resolution.DAILY,
        period=Period.HISTORICAL
    )

    print(next(stations.all().values.query()))

Get data for a parameter:

.. ipython:: python
    :okwarning:

    from wetterdienst import Resolution, Period
    from wetterdienst.provider.dwd.observation import DwdObservationParameter

    observation_data = DwdObservationRequest(
        parameter=DwdObservationParameter.DAILY.PRECIPITATION_HEIGHT,
        resolution=Resolution.DAILY,
        period=Period.HISTORICAL
    )

    print(next(stations.all().values.query()))

Get data for a parameter from another dataset:

.. ipython:: python
    :okwarning:

    from wetterdienst import Resolution, Period
    from wetterdienst.provider.dwd.observation import DwdObservationRequest

    observation_data = DwdObservationRequest(
        parameter=[("precipitation_height", "precipitation_more")],
        resolution=Resolution.DAILY,
        period=Period.HISTORICAL
    )

    print(next(stations.all().values.query()))

Mosmix
======

Get stations for MOSMIX-SMALL:

.. ipython:: python
    :okwarning:

    from wetterdienst import Resolution, Period
    from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest, DwdMosmixType

    stations = DwdMosmixRequest(parameter="large", mosmix_type=DwdMosmixType.LARGE)

    print(stations.all().df.head())

Get data for MOSMIX-LARGE:

.. ipython:: python
    :okwarning:

    from wetterdienst import Resolution, Period
    from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest, DwdMosmixType

    stations = DwdMosmixRequest(parameter="large", mosmix_type=DwdMosmixType.LARGE).filter_by_station_id(
        station_id=["01001", "01008"]
    )

    print(stations.values.all().df.head())

Radar
=====

Sites
-----

Retrieve information about all OPERA radar sites.

.. ipython:: python
    :okwarning:

    from wetterdienst.provider.eumetnet.opera.sites import OperaRadarSites

    # Acquire information for all OPERA sites.
    sites = OperaRadarSites().all()
    print(f"Number of OPERA radar sites: {len(sites)}")

    # Acquire information for a specific OPERA site.
    site_ukdea = OperaRadarSites().by_odim_code("ukdea")
    print(site_ukdea)

Retrieve information about the DWD radar sites.

.. ipython:: python
    :okwarning:

    from wetterdienst.provider.dwd.radar.api import DwdRadarSites

    # Acquire information for a specific site.
    site_asb = DwdRadarSites().by_odim_code("ASB")
    print(site_asb)

Data
----

To use ``DWDRadarRequest``, you have to provide a ``RadarParameter``,
which designates the type of radar data you want to obtain. There is
radar data available at different locations within the DWD data repository:

- https://opendata.dwd.de/weather/radar/composite/
- https://opendata.dwd.de/weather/radar/radolan/
- https://opendata.dwd.de/weather/radar/radvor/
- https://opendata.dwd.de/weather/radar/sites/
- https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/radolan/
- https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/
- https://opendata.dwd.de/climate_environment/CDC/grids_germany/5_minutes/radolan/

For ``RADOLAN_CDC``-data, the time resolution parameter (either hourly or daily)
must be specified.

The ``date_times`` (list of datetimes or strings) or a ``start_date``
and ``end_date`` parameters can optionally be specified to obtain data
from specific points in time.

For ``RADOLAN_CDC``-data, datetimes are rounded to ``HH:50min``, as the
data is packaged for this minute step.

This is an example on how to acquire ``RADOLAN_CDC`` data using
``wetterdienst`` and process it using ``wradlib``.

For more examples, please have a look at `examples/radar/`_.

.. code-block:: python

    from wetterdienst.provider.dwd.radar import DwdRadarValues, DwdRadarParameter, DwdRadarResolution
    import wradlib as wrl

    radar = DwdRadarValues(
        radar_parameter=DwdRadarParameter.RADOLAN_CDC,
        resolution=DwdRadarResolution.DAILY,
        start_date="2020-09-04T12:00:00",
        end_date="2020-09-04T12:00:00"
    )

    for item in radar.query():

        # Decode item.
        timestamp, buffer = item

        # Decode data using wradlib.
        data, attributes = wrl.io.read_radolan_composite(buffer)

        # Do something with the data (numpy.ndarray) here.

.. _examples/radar/: https://github.com/earthobservations/wetterdienst/tree/main/examples/radar
