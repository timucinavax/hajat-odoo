from odoo import http

class CustomController(http.Controller):
    @http.route('/web_editor/iframe', type='http', auth='user')
    def web_editor_iframe(self, **kwargs):
        response = http.request.render('website.web_editor_iframe', {})
        response.headers['Content-Security-Policy'] = "upgrade-insecure-requests"
        return response