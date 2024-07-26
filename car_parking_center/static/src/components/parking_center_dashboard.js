/** @odoo-module **/

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart, useState } = owl

export class ParkingCenterDashboard extends Component {
    setup(){
        this.state = useState({
            quotations: {
                parked_lot: 0,
                free_lot: 0,
                reserved_lot: 0,
                total_visit: 0,
                total_payment: 0,
            }
        })
        this.orm = useService("orm")

        onWillStart( async ()=>{
            await this.getQuotations()
        })
    }

    async getQuotations(){
        this.state.quotations.parked_lot = await this.orm.searchCount("parking.center.visit", [['state', '=', 'parked']])
        this.state.quotations.free_lot = await 100-this.state.quotations.parked_lot
        this.state.quotations.reserved_lot = await this.orm.searchCount("parking.center.visit", [['state', '=', 'reserved']])
        this.state.quotations.total_visit = await this.orm.searchCount("parking.center.visit", [])
        const total_payment = await this.orm.readGroup("parking.center.payment", [], ["amount:sum"], [])
        this.state.quotations.total_payment = total_payment[0].amount
    }
}

ParkingCenterDashboard.template = "car_parking_center.ParkingCenterDashboard"
ParkingCenterDashboard.components = { KpiCard }

registry.category("actions").add("car_parking_center.parking_center_dashboard", ParkingCenterDashboard)
