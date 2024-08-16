from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_status = fields.Selection([
        ('placed', 'Order Placed'),
        ('confirmed', 'Order Confirmed'),
        ('preparing', 'Preparing Order'),
        ('ready', 'Ready for Pickup'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('delayed', 'Delayed'),
        ('partially_delivered', 'Partially Delivered'),
        ('returned', 'Returned'),
    ], string='Custom Status', default='placed')

    def action_confirm_order(self):
        if self.custom_status != 'placed':
            raise UserError("You can only confirm an order that has been placed.")
        self.write({'custom_status': 'confirmed'})
        self.action_confirm()  # Confirm the order and create delivery order

    def action_prepare_order(self):
        if self.custom_status != 'confirmed':
            raise UserError("You can only prepare an order that has been confirmed.")
        self.write({'custom_status': 'preparing'})
        for picking in self.picking_ids:
            picking.action_assign()  # Reserve products

    def action_ready_for_pickup(self):
        if self.custom_status != 'preparing':
            raise UserError("You can only mark an order as ready for pickup after it has been prepared.")
        self.write({'custom_status': 'ready'})
        # Additional logic if needed

    def action_out_for_delivery(self):
        if self.custom_status != 'ready':
            raise UserError("You can only mark an order as out for delivery if it is ready for pickup.")
        self.write({'custom_status': 'out_for_delivery'})
        for picking in self.picking_ids:
            picking.button_validate()  # Mark delivery as done

    def action_delivered(self):
        if self.custom_status != 'out_for_delivery':
            raise UserError("You can only mark an order as delivered if it is out for delivery.")
        self.write({'custom_status': 'delivered'})
        # Additional logic if needed

    def action_cancel_order(self):
        if self.custom_status in ['delivered', 'returned']:
            raise UserError("You cannot cancel an order that has already been delivered or returned.")
        self.write({'custom_status': 'cancelled'})
        self.action_cancel()  # Cancel the order and delivery

    def action_delay_order(self):
        if self.custom_status not in ['preparing', 'ready', 'out_for_delivery']:
            raise UserError("You can only delay an order that is being prepared, ready for pickup, or out for delivery.")
        self.write({'custom_status': 'delayed'})
        # Notify the customer if needed

    def action_partially_deliver(self):
        if self.custom_status != 'out_for_delivery':
            raise UserError("You can only mark an order as partially delivered if it is out for delivery.")
        self.write({'custom_status': 'partially_delivered'})
        # Split the picking if needed

    def action_return_order(self):
        if self.custom_status != 'delivered':
            raise UserError("You can only return an order that has been delivered.")
        self.write({'custom_status': 'returned'})
        # Create return picking
        self._create_return_picking()

    def _create_return_picking(self):
        for picking in self.picking_ids:
            return_picking = picking.copy({
                'picking_type_id': self.env.ref('stock.picking_type_in').id,
                'origin': picking.name,
                'move_ids_without_package': [
                    (0, 0, {
                        'name': move.name,  # Set the name field from the existing move
                        'product_id': move.product_id.id,
                        'product_uom_qty': move.product_uom_qty,
                        'product_uom': move.product_uom.id,
                        'location_id': move.location_dest_id.id,
                        'location_dest_id': move.location_id.id,
                        'picking_id': False,
                    }) for move in picking.move_ids_without_package
                ]
            })
            return_picking.action_confirm()
            return_picking.action_assign()
            return_picking.button_validate()

