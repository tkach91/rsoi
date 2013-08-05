/*
 * File: app/store/JCatalogue.js
 *
 * This file was generated by Sencha Architect version 2.1.0.
 * http://www.sencha.com/products/architect/
 *
 * This file requires use of the Ext JS 4.1.x library, under independent license.
 * License of Sencha Architect does not include license for Ext JS 4.1.x. For more
 * details see http://www.sencha.com/license or contact license@sencha.com.
 *
 * This file will be auto-generated each and everytime you save your project.
 *
 * Do NOT hand edit this file.
 */

Ext.define('Catalogue.store.JCatalogue', {
	extend: 'Ext.data.Store',

	requires: [
		'Catalogue.model.Catalogue'
	],

	constructor: function(cfg) {
		var me = this;
		cfg = cfg || {};
		me.callParent([Ext.apply({
			storeId: 'JCatalogueID',
			model: 'Catalogue.model.Catalogue',
			autoSync: true,
			listeners: {
				load: function(store, records, successful, eOpts ) {
					model = Ext.ModelManager.getModel('Catalogue.model.Catalogue');
					store.insert(0, model.create({ }));
				},
				write: function (store, operation, eOpts) {
					if (operation.action == 'create') {
						model = Ext.ModelManager.getModel('Catalogue.model.Catalogue');
						store.insert(0, model.create({ }));
					}
				}
			},
			proxy: {
				type: 'ajax',
				url: '/catalogue_admin',
				api: {
					create  : '/catalogue_admin/create',
					read    : '/catalogue_admin/read',
					update  : '/catalogue_admin/update',
					destroy : '/catalogue_admin/destroy'
				},
				reader: {
					type: 'json',
					idProperty: 'id',
					root: 'root'
				},
				writer: {
					type: 'json',
					writeAllFields: false,
					root: 'root'
				}
			}
		}, cfg)]);
	}
});
