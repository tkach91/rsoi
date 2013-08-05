/*
 * File: app/model/PostService.js
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

Ext.define('POSTMan.model.PostService', {
	extend: 'Ext.data.Model',

	fields: [
		{
			name: 'id',
			type: 'int'
		},
		{
			name: 'idExternal',
			type: 'int'
		},
		{
			name: 'address',
			type: 'string'
		},
		{
			name: 'date',
			type: 'date'
		},
		{
			name: 'server',
			type: 'string'
		},
		{
			name: 'status',
			type: 'string'
		}
	],
	validations: [
		{
			type: 'length',
			field: 'address',
			min: 1
		}, {
			type: 'length',
			field: 'date',
			min: 1
		}
	]
});