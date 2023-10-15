<!DOCTYPE html>
<html>
<head>
    <title>Manual Charging Configuration for Solax Inverter (Modbus v. 2023.09.07)</title>
</head>
<body>
    <h1>Manual Charging Configuration for Solax Inverter (Modbus v. 2023.09.07)</h1>

    <p>This guide will walk you through the process of configuring manual charging for your Solax Inverter with Modbus version 2023.09.07. Manual charging allows you to control when your inverter charges your battery.</p>

    <h2>Prerequisites</h2>

    <p>Before you begin, make sure you have the following prerequisites:</p>

    <ul>
        <li>The latest version of Solax Inverter Modbus (v. 2023.09.07) installed and configured.</li>
        <li>Home Assistant or a similar home automation platform.</li>
    </ul>

    <h2>Step 1: Create Helpers</h2>

    <ol>
        <li>Create three helpers of the following types:</li>
        <ul>
            <li><code>input_datetime.growatt_start_time</code> (Type: Time)</li>
            <li><code>input_datetime.growatt_end_time</code> (Type: Time)</li>
            <li><code>input_boolean.start_growatt_charge</code></li>
        </ul>
    </ol>

    <h2>Step 2: Create an Automation</h2>

    <p>Create an automation to trigger manual charging based on your specified start and end times. Replace <code>&lt;integration_name_solax&gt;</code> with the name of your Solax integration. You can find this name in your Home Assistant configuration.</p>

    <pre><code>
alias: Growatt Battery Charge (Manual)
description: Manual battery charging control for Solax Inverter
trigger:
  - platform: state
    entity_id: input_boolean.start_growatt_charge
    to: "on"
action:
  - service: select.select_option
    data_template:
      entity_id: select.&lt;integration_name_solax&gt;_charger_start_time_1
      option: &gt;-
        {{ states('input_datetime.growatt_start_time') |
        regex_replace(':[0-9]{2}$', '') }}
    enabled: true
  - service: select.select_option
    data_template:
      entity_id: select.&lt;integration_name_solax&gt;_charger_end_time_1
      option: &gt;-
        {{ states('input_datetime.growatt_end_time') |
        regex_replace(':[0-9]{2}$', '') }}
  - device_id: select.&lt;integration_name_solax&gt;_charger_switch
    domain: select
    entity_id: select.&lt;integration_name_solax&gt;_charger_switch
    type: select_option
    option: Enabled
    enabled: true
  - device_id: select.&lt;integration_name_solax&gt;_charger_time_1
    domain: select
    entity_id: select.&lt;integration_name_solax&gt;_charger_time_1
    type: select_option
    option: Enabled
  - service: input_boolean.turn_off
    entity_id: input_boolean.start_growatt_charge
mode: single
    </code></pre>

    <p>Make sure to replace <code>&lt;integration_name_solax&gt;</code> with the actual name of your Solax integration.</p>

    <h2>Step 3: Create a Dashboard Element</h2>

    <p>Add the following dashboard element to your Home Assistant dashboard to control manual charging:</p>

    <pre><code>
type: entities
entities:
  - entity: input_datetime.growatt_start_time
  - entity: input_datetime.growatt_end_time
  - entity: input_boolean.start_growatt_charge
title: Battery Charging Control
    </code></pre>

    <p>This dashboard element will allow you to set the start and end times for manual charging and initiate the charging process by toggling the <code>start_growatt_charge</code> switch.</p>

    <p>That's it! You've successfully configured manual charging for your Solax Inverter Modbus (v. 2023.09.07) using Home Assistant.</p>
</body>
</html>
