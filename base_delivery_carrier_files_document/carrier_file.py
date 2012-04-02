# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2012 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64

from osv import osv, fields


class carrier_file(osv.osv):
    _inherit = 'delivery.carrier.file'

    def get_write_mode_selection(self, cr, uid, context=None):
        res = super(carrier_file, self).get_write_mode_selection(cr, uid, context=context)
        if 'document' not in res:
            res.append(('document', 'Document'))
        return res

    _columns = {
        'write_mode': fields.selection(get_write_mode_selection, 'Write on', required=True),
        'document_directory_id': fields.many2one('document.directory', 'Document Directory'),
        'export_path': fields.char('Export Path', size=256),
    }

    def _prepare_attachment(self, carrier_file, filename, file_content, context=None):
        return {'name': "%s_%s" % (carrier_file.name, filename),
                'datas_fname': filename,
                'datas': base64.encodestring(file_content),
                'parent_id': carrier_file.document_directory_id.id,
                'type': 'binary'}

    def _write_file(self, cr, uid, carrier_file, filename, file_content, context=None):
        if carrier_file.write_mode == 'document':
            vals = self._prepare_attachment(carrier_file, filename, file_content)
            self.pool.get('ir.attachment').create(cr, uid, vals, context=context)
            return True
        else:
            return (super(carrier_file, self)
                    ._write_file(cr, uid, carrier_file, filename, file_content, context=None))

carrier_file()
