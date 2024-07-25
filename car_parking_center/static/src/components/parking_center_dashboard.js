/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card";
const { Component } = owl;

export class ParkingCenterDashboard extends Component {}

ParkingCenterDashboard.template = "car_parking_center.ParkingCenterDashboard"
ParkingCenterDashboard.components = { KpiCard }

registry.category("actions").add("car_parking_center.parking_center_dashboard", ParkingCenterDashboard)
