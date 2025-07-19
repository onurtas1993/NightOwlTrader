<table>
  <tr>
    <td>

<img src="./resources/icon.ico" width="128"/>
    </td>
    <td>

# Night Owl Trader

Automated trading assistant designed to help you analyze, simulate, and execute trading strategies on various financial instruments.
    </td>
  </tr>
</table>

<img src="https://www.dropbox.com/scl/fi/fymw6fqc7pidsgty3cr18/banner.jpg?rlkey=u03o63g15mfr75wuox3shzg91&raw=1" width="922"/>

---

<img src="https://www.dropbox.com/scl/fi/3b7v6jahujl8bzqcvwo74/banner2.jpg?rlkey=rsiew3lw7lqqbdui6r85cuhvb&raw=1" width="922"/>

## Getting Started

To run the app locally:

1. **Create a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```sh
   python ./app_main.py
   ```

---

## Features

- **Algorithmic Trading**: Plug-and-play trading algorithms with customizable parameters.
- **Order Management**: Place, track, and manage buy/sell orders with advanced options.
- **Simulation & Backtesting**: Simulate potential profits and visualize trading signals on historical data.
- **Robust Error Handling**: Handles insufficient balances, non-existent coins, and retry logic for failed orders.
- **User-Friendly Interface**: Real-time charting and clear application state indicators in the GUI.

---

## Example Use Cases

- **Conditional Orders**:  
  _"Buy BTC if it hits 90k USD. Sell BTC if it hits 110k USD."_

- **Autopilot Management**:  
  Add or remove assets from autopilot trading without lingering background processes.

- **Retry Limits**:  
  Automatically stop retrying failed orders after a configurable number of attempts.

---

## To Do List

- [ ] **Enter the time interval for intelli option**  
  _Example: 4h for 4hour data 6h for 6hour data.._

- [x] **Enter an order with a target price**  
  _Example: Buy BTC if it hits 90k USD. Sell BTC if it hits 110k USD._

- [x] **Bugfix: Removing an order stops its processing**  
  _Example: Add ETH autopilot, delete ETH, it should stop processing ETH._

- [ ] **Add `max_try_limit` parameter for each order**  
  _Example: Stop retrying to buy a non-existent coin after X attempts._

- [x] **Handle insufficient balance with `sell_available` and `buy_available` methods**  
  _Example: Sell as much as available if full amount is not present._

- [x] **Show application state in the main GUI**  
  _Example: Banner at the bottom shows green (active) or red (inactive)._

- [ ] **Fix Remote CSV analysis functionality**  
  _Example: Click the Remote CSV button and it should work._

---

## Project Structure

Below is the current class/package structure of the project which shows the MVC architecture:  
importnat note: Some of the class members are hidden due to their less importance and space management for the chart.

![UML Diagram](https://raw.githubusercontent.com/gist/onurtas1993/511276d006006e7e3698660fea8862a5/raw/4dd2d0f720da0b1c16df561091167aae843e5d47/uml.svg)

---

## Notes

- There is a `sample.csv` file located in the main folder of the repository.  
  This file contains Wheat Daily data sourced from FOREXCOM and can be used for testing for "Local CSV" functionality.
- **If you plan to use the Binance API, you must enter your API keys in the `config/config.json` file.**

