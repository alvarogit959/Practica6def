from odoo import models

class ReportRepartoPendientes(models.AbstractModel):
    _name = 'report.empresa_reparto.report_repartos_pendientes_empleado'
    _description = 'Reporte de Repartos Pendientes'

    def _get_report_values(self, docids, data=None):
        docs = self.env['reparto.empleado'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'reparto.empleado',
            'docs': docs,
        }