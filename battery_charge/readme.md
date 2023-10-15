# Manual Charging Configuration for Solax Inverter (Modbus v. 2023.09.07)

This guide will walk you through the process of configuring manual charging for your Solax Inverter with Modbus version 2023.09.07. Manual charging allows you to control when your inverter charges your battery.

## Prerequisites

Before you begin, make sure you have the following prerequisites:

- The latest version of Solax Inverter Modbus (v. 2023.09.07) installed and configured.
- Home Assistant or a similar home automation platform.

## Step 1: Create Helpers

1. Create three helpers of the following types:

   - `input_datetime.growatt_start_time` (Type: Time)
   - `input_datetime.growatt_end_time` (Type: Time)
   - `input_boolean.start_growatt_charge`

## Step 2: Create an Automation

Create an automation to trigger manual charging based on your specified start and end times. Replace `<integration_name_solax>` with the name of your Solax integration. You can find this name in your Home Assistant configuration.

```yaml
alias: Growatt Battery Charge (Manual)
description: Manual battery charging control for Solax Inverter
trigger:
  - platform: state
    entity_id: input_boolean.start_growatt_charge
    to: "on"
action:
  - service: select.select_option
    data_template:
      entity_id: select.<integration_name_solax>_charger_start_time_1
      option: >-
        {{ states('input_datetime.growatt_start_time') |
        regex_replace(':[0-9]{2}$', '') }}
    enabled: true
  - service: select.select_option
    data_template:
      entity_id: select.<integration_name_solax>_charger_end_time_1
      option: >-
        {{ states('input_datetime.growatt_end_time') |
        regex_replace(':[0-9]{2}$', '') }}
  - device_id: select.<integration_name_solax>_charger_switch
    domain: select
    entity_id: select.<integration_name_solax>_charger_switch
    type: select_option
    option: Enabled
    enabled: true
  - device_id: select.<integration_name_solax>_charger_time_1
    domain: select
    entity_id: select.<integration_name_solax>_charger_time_1
    type: select_option
    option: Enabled
  - service: input_boolean.turn_off
    entity_id: input_boolean.start_growatt_charge
mode: single
```


Make sure to replace <integration_name_solax> with the actual name of your Solax integration.

## Step 3: Create a Dashboard Element

Add the following dashboard element to your Home Assistant dashboard to control manual charging:

```type: entities
entities:
  - entity: input_datetime.growatt_start_time
  - entity: input_datetime.growatt_end_time
  - entity: input_boolean.start_growatt_charge
title: Battery Charging Control
```
