Configuration File zipline-trader.yaml
=========================================

| In order to run this package you could use the following config file or environment variables, Whatever you prefer.

Module Configuration (Why?)
-----------------------------

| This package has moving parts as described below:

| * Data provider to use, and data provider credentials
| * Universe selection
| * Backend preferences (which DB to use, where it's located)

| This is why we put everything in a configuration file

Config File Location
))))))))))))))))))))))))

| After some feedback from the community this next approach was chosen to make it easier to find the configuration file.  The recommended file name is ``ziplint-trader.yaml``, but you could select what ever you prefer.
| You need to set this environment variable to tell the package where to locate the config file: ``ZIPLINE_TRADER_CONFIG``
| So for instance:

.. code-block::

    export ZIPLINE_TRADER_CONFIG=./zipline-trader.yaml

Sample Config file
----------------------

.. code-block:: yaml

    alpaca:
      key_id: "<YOUR-KEY>"
      secret: "<YOUR-SECRET>"
      base_url: https://paper-api.alpaca.markets
      universe: SP500
      custom_asset_list: AAPL, TSLA, GOOG

    alpha-vantage:
      ALPHAVANTAGE_API_KEY: "<YOUR-KEY>"
      AV_FREQ_SEC: 60
      AV_CALLS_PER_FREQ: 5
      AV_TOLERANCE_SEC: 1

    backend:
      type: postgres
      postgres:
        host: 127.0.0.1
        port: 5439
        user: postgres
        password: postgres


..

Tutorial Video
-------------------

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/-lDPNX2SbYU" frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen></iframe>