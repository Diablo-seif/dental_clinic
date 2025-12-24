/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class DashboardAction extends Component {
static template = "dental_clinic.dashboardXML";
}


registry.category("actions").add("dental_clinic.dashboardJS", DashboardAction);


