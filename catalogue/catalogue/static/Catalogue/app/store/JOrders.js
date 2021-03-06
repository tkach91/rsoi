/*
 * File: app/store/JOrders.js
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

Ext.define('Catalogue.store.JOrders', {
	extend: 'Ext.data.Store',

	requires: [
		'Catalogue.model.Orders'
	],

	constructor: function(cfg) {
		var me = this;
		cfg = cfg || {};
		me.callParent([Ext.apply({
			storeId: 'JOrdersID',
			model: 'Catalogue.model.Orders',
			autoSync: true,
			proxy: {
				type: 'ajax',
				url: '/orders',
				api: {
					create  : '/orders/create',
					read    : '/orders/read',
					update  : '/orders/update',
					destroy : '/orders/destroy'
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
