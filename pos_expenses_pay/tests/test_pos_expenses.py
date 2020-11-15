# Copyright 2019 Ilmir Karamov <https://it-projects.info/team/ilmir-k>
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).
import odoo.tests
from odoo.api import Environment


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):
    def test_pos_expenses_pay(self):
        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        cr = self.registry.cursor()
        env = Environment(cr, self.uid, {})
        env["ir.module.module"].search(
            [("name", "=", "pos_expenses_pay")], limit=1
        ).state = "installed"
        cr.release()

        self.phantom_js(
            "/web",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('pos_expenses_pay_tour', 500)",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_expenses_pay_tour.ready",
            login="admin",
            timeout=100,
        )