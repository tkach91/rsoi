/*
 * File: app/store/JPostService.js
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

Ext.define('POSTMan.store.JPostService', {
	extend: 'Ext.data.Store',

	requires: [
		'POSTMan.model.PostService'
	],

	constructor: function(cfg) {
		var me = this;
		cfg = cfg || {};
		me.callParent([Ext.apply({
			storeId: 'JPostServiceID',
			model: 'POSTMan.model.PostService',
			autoSync: true,
			listeners: {
				load: function(store, records, successful, eOpts ) {
					model = Ext.ModelManager.getModel('POSTMan.model.PostService');
					store.insert(0, model.create({ status: 'decline' }));
				},
				write: function (store, operation, eOpts) {
					if (operation.action == 'create') {
						model = Ext.ModelManager.getModel('POSTMan.model.PostService');
						store.insert(0, model.create({ status: 'decline' }));
					}
				}
			},
			proxy: {
				type: 'ajax',
				url: '/',
				api: {
					create  : '/postman/create',
					read    : '/postman/read',
					update  : '/postman/update',
					destroy : '/postman/destroy'
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
