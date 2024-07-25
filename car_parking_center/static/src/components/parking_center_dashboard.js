/** @odoo-module **/

import { registry } from "@web/core/registry";
const { Component } = owl;

export class ParkingCenterDashboard extends Component {}

ParkingCenterDashboard.template = "car_parking_center.ParkingCenterDashboard"

registry.category("actions").add("car_parking_center.parking_center_dashboard", ParkingCenterDashboard)
