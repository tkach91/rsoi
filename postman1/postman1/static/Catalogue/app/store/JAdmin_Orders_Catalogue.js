/*
 * File: app/store/JAdmin_Orders_Catalogue.js
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

Ext.define('Catalogue.store.JAdmin_Orders_Catalogue', {
	extend: 'Ext.data.Store',

	requires: [
		'Catalogue.model.Orders_Catalogue'
	],

	constructor: function(cfg) {
		var me = this;
		cfg = cfg || {};
		me.callParent([Ext.apply({
			storeId: 'JAdmin_Orders_CatalogueID',
			model: 'Catalogue.model.Orders_Catalogue',
			autoSync: true,
			proxy: {
				type: 'ajax',
				url: '/orders_catalogue',
				api: {
					create  : '/orders_catalogue/create',
					read    : '/orders_catalogue/read',
					update  : '/orders_catalogue/update',
					destroy : '/orders_catalogue/destroy'
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
