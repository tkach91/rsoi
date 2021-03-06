/*
 * File: app/view/MyPanel3.js
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

var authorized;
var username_;
Ext.define('Catalogue.view.Catalogue', {
	extend: 'Ext.panel.Panel',

	height: 500,
	width: 560,
	layout: {
		type: 'border'
	},

	initComponent: function() {
		var me = this;
		Ext.applyIf(me, {
			items: [
				{
					xtype: 'tabpanel',
					region: 'center',
					activeTab: 0,
					items: [
						{
							xtype: 'panel',
							layout: {
								type: 'border'
							},
							title: 'Catalogue List',
							items: [
								{
									xtype: 'gridpanel',
									region: 'center',
									id: 'Catalogue.gridPanel.Catalogue',
									store: 'JCatalogue',
									listeners:{
										viewready: function(grid) {
											var store = grid.getStore();
											store.load();
										}
									},
									viewConfig: {

									},
									plugins: [Ext.create('Ext.grid.plugin.CellEditing', {
										clicksToEdit: 1,
									})],
									columns: [
										{
											xtype: 'gridcolumn',
											hidden: true,
											dataIndex: 'id',
											text: 'Id'
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'name',
											text: 'Name',
											editor: {
												xtype: 'textfield'
											},
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Name</span>';
												return value;
											}
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'description',
											text: 'Description',
											editor: {
												xtype: 'textfield'
											},
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Description</span>';
												return value;
											}
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'price',
											text: 'Price',
											editor: {
												xtype: 'numberfield'
											},
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Price</span>';
												return value;
											}
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'idCatalogue',
											text: 'idCatalogue',
											editor: { xtype:'numberfield' },
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Id Catalogue</span>';
												return value;
											}
										},
										{
											xtype: 'actioncolumn',
											width:50,
											items: [
											{
												icon: '/static/resources/fam/delete.gif',
												tooltip: 'Delete',
												handler: function(grid, rowIndex, colIndex, item, e, record) {
													if (record.get('price') > 0) {
														Ext.MessageBox.confirm('Alert', 'Delete item?', function(btn) {
															if (btn == 'yes') {
																var store = grid.getStore();
																store.remove(record);
															}
														});
													}
												}
											},
											{
												icon: '/static/resources/fam/add.gif',
												tooltip: 'Add',
												handler: function(grid, rowIndex, colIndex, item, e, record) {
													console.log(record.get('idCatalogue'));
													if (record.get('price') > 0) {
														if ((record.get('amount') == undefined) || (record.get('amount') == 0) || (record.get('amount') == null)) {
															Ext.MessageBox.confirm('Add', 'Add only one item?', function(btn) {
																if (btn == 'yes') {
																	store = Ext.getCmp('Catalogue.gridPanel.Orders_Catalogue').getStore();
																	model = Ext.ModelManager.getModel('Catalogue.model.Orders_Catalogue');
																	store.insert(0, model.create({ count: 1, idCatalogue: record.get('idCatalogue'), idOrder: undefined }));
																}
															});
															return;
														}
														store = Ext.getCmp('Catalogue.gridPanel.Orders_Catalogue').getStore();
														model = Ext.ModelManager.getModel('Catalogue.model.Orders_Catalogue');
														store.insert(0, model.create({ count: record.get('amount'), idCatalogue: record.get('idCatalogue'), idOrder: undefined }));
														record.set('amount', undefined)
													}
												}
											}
											]
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'amount',
											text: 'Amount',
											editor: {
												xtype: 'numberfield'
											},
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Amount</span>';
												return value;
											}
										}
									]
								}
							]
						},
						{
							xtype: 'panel',
							layout: {
								type: 'border'
							},
							title: 'Check Out',
							items: [
								{
									xtype: 'gridpanel',
									region: 'center',
									id: 'Catalogue.gridPanel.Orders_Catalogue',
									store: 'JOrders_Catalogue',
									viewConfig: {

									},
									plugins: [Ext.create('Ext.grid.plugin.CellEditing', {
										clicksToEdit: 1,
									})],
									columns: [
										{
											xtype: 'gridcolumn',
											dataIndex: 'idOrder',
											text: 'IdOrder',
											hidden: true
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'idCatalogue',
											text: 'Description',
											renderer: function(value, metaData, record) {
												store = Ext.getCmp('Catalogue.gridPanel.Catalogue').getStore();
												product = store.findRecord('idCatalogue', value, 0, false, false, true);
												return product.get('description');
											}
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'count',
											text: 'Count',
											editor: {
												xtype: 'numberfield'
											}
										},
										{
											xtype: 'gridcolumn',
											text: 'Price',
											renderer: function(value, metaData, record) {
												store = Ext.getCmp('Catalogue.gridPanel.Catalogue').getStore();
												product = store.findRecord('idCatalogue', record.get('idCatalogue'), 0, false, false, true);
												return product.get('price') * record.get('count');
											}
										},
										{
											xtype: 'actioncolumn',
											width:50,
											items: [
											{
												icon: '/static/resources/fam/delete.gif',
												tooltip: 'Delete',
												handler: function(grid, rowIndex, colIndex, item, e, record) {
													if (record.get('count') > 0) {
														Ext.MessageBox.confirm('Alert', 'Delete item?', function(btn) {
															if (btn == 'yes') {
																var store = grid.getStore();
																store.remove(record);
															}
														});
													}
												}
											}
											]
										}
									]
								},
								{
									xtype: 'form',
									id: 'Catalogue.form',
									disabled: !(document.authorized),
									region: 'south',
									height: 150,
									bodyPadding: 10,
									items: [
										{
											xtype: 'textareafield',
											anchor: '100%',
											fieldLabel: 'Where?',
											id: 'Catalogue.form.south.address'
										},
										{
											xtype: 'datefield',
											anchor: '100%',
											fieldLabel: 'When?',
											id: 'Catalogue.form.south.date'
										},
										{
											xtype: 'hidden',
											id: 'Catalogue.form.south.idOrder',
											listeners: {
												change: function( field, newValue, oldValue, eOpts ) {
													store_ = Ext.getCmp('Catalogue.gridPanel.Orders_Catalogue').getStore();
													store_.suspendAutoSync();
													store_.each(function(item, index, count) {
														item.set('idOrder', newValue);
													});
													store_.sync({
														callback: function() {
															store_ = Ext.getCmp('Catalogue.gridPanel.Orders_Catalogue').getStore();
															store_.resumeAutoSync();
															store_.load({
																params: {
																	fakeLoad: true
																}
															});
														}
													});
													
													address = Ext.getCmp('Catalogue.form.south.address').setValue('');
													date = Ext.getCmp('Catalogue.form.south.date').setValue('');
													Ext.getCmp('Catalogue.toolbar.suma').setText('');
													Ext.getCmp('Catalogue.toolbar.amount').setText('');
												}
											}
										},
										{
											xtype: 'button',
											text: 'Submit Order',
											handler: function() {
												store = Ext.getCmp('Catalogue.gridPanel.Orders').getStore();
												model = Ext.ModelManager.getModel('Catalogue.model.Orders');
												
												address = Ext.getCmp('Catalogue.form.south.address').getValue();
												date = Ext.getCmp('Catalogue.form.south.date').getValue();
												idOrder = Ext.getCmp('Catalogue.form.south.idOrder').getValue();
												
												store.suspendAutoSync();
												store.insert(0, model.create({ address: address, date: date }));
												store.sync({
													callback: function() {
														store = Ext.getCmp('Catalogue.gridPanel.Orders').getStore();
														store.resumeAutoSync();
													},
													success: function(batch, opts) {
														idOrder = batch.operations[0].records[0].get('id');
														Ext.getCmp('Catalogue.form.south.idOrder').setValue(idOrder);
													}
												})
											}
										},
										{
											xtype: 'button',
											text: 'Clear Order',
											handler: function() {
												store_ = Ext.getCmp('Catalogue.gridPanel.Orders_Catalogue').getStore();
												store_.load({
													params: {
														fakeLoad: true
													}
												});
												address = Ext.getCmp('Catalogue.form.south.address').setValue('');
												date = Ext.getCmp('Catalogue.form.south.date').setValue('');
												Ext.getCmp('Catalogue.toolbar.suma').setText('');
												Ext.getCmp('Catalogue.toolbar.amount').setText('');
											}
										}
									]
								}
							]
						},
						{
							xtype: 'panel',
							id: 'Catalogue.gridPanel.OrderStatus',
							disabled: !(document.authorized),
							layout: {
								type: 'border'
							},
							title: 'Order Status',
							items: [
								{
									xtype: 'gridpanel',
									region: 'center',
									id: 'Catalogue.gridPanel.Orders',
									store: 'JOrders',
									viewConfig: {

									},
									plugins: [Ext.create('Ext.grid.plugin.CellEditing', {
										clicksToEdit: 1,
									})],
									columns: [
										{
											xtype: 'gridcolumn',
											hidden: true,
											dataIndex: 'id',
											text: 'Id'
										},
										{
											xtype: 'gridcolumn',
											hidden: true,
											dataIndex: 'idUser',
											text: 'IdUser'
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'address',
											text: 'Address',
											editor: {
												xtype: 'textfield'
											},
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Address</span>';
												return value;
											}
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'date',
											text: 'Date',
											editor: {
												xtype: 'datefield'
											},
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Date</span>';
												return value;
											}
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'status',
											text: 'Status',
											editor: {
												xtype: 'textfield'
											},
											renderer: function(value) {
												if ((value == 0) || (value == '') || (value == undefined) || (value == null))
													return '<span style="color:gray;">Status</span>';
												return value;
											},
											editor: {
												xtype: 'combobox',
												displayField: 'status',
												valueField: 'status',
												store: Ext.create('Ext.data.Store', {
													fields: ['status'],
													data : [
														{'status': 'accepted'},
														{'status': 'declined'},
														{'status': 'reserved'},
														{'status': 'delivering'},
														{'status': 'canceled'},
													]
												}),
												typeAhead: true
											}
										},
										{
											xtype: 'actioncolumn',
											width:50,
											items: [
											{
												icon: '/static/resources/fam/delete.gif',
												tooltip: 'Delete',
												handler: function(grid, rowIndex, colIndex, item, e, record) {
													Ext.MessageBox.confirm('Alert', 'Delete item?', function(btn) {
														if (btn == 'yes') {
															var store = grid.getStore();
															store.remove(record);
														}
													});
													
												}
											},
											{
												icon: '/static/resources/fam/14_layer_novisible.png',
												tooltip: 'Show',
												handler: function(grid, rowIndex, colIndex, item, e, record) {
													var store = Ext.getCmp('Catalogue.gridPanel.Admin_Orders_Catalogue').getStore();
													store.load({
														params: {
															idOrder: record.get('id')
														}
													});
												}
											}
											]
										}
									]
								},
								{
									xtype: 'gridpanel',
									region: 'south',
									height: 150,
									id: 'Catalogue.gridPanel.Admin_Orders_Catalogue',
									store: 'JAdmin_Orders_Catalogue',
									viewConfig: {

									},
									plugins: [Ext.create('Ext.grid.plugin.CellEditing', {
										clicksToEdit: 1,
									})],
									columns: [
										{
											xtype: 'gridcolumn',
											dataIndex: 'idOrder',
											text: 'IdOrder',
											hidden: true
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'idCatalogue',
											text: 'Description',
											renderer: function(value, metaData, record) {
												store = Ext.getCmp('Catalogue.gridPanel.Catalogue').getStore();
												product = store.findRecord('id', value, 0, false, false, true);
												return product.get('description');
											}
										},
										{
											xtype: 'gridcolumn',
											dataIndex: 'count',
											text: 'Count'
										},
										{
											xtype: 'gridcolumn',
											text: 'Price',
											renderer: function(value, metaData, record) {
												store = Ext.getCmp('Catalogue.gridPanel.Catalogue').getStore();
												product = store.findRecord('id', record.get('idCatalogue'), 0, false, false, true);
												return product.get('price') * record.get('count');
											}
										}
									]
								}
							]
						}
					],
					dockedItems: [
						{
							xtype: 'toolbar',
							dock: 'bottom',
							items: [
								{
									xtype: 'tbseparator'
								},
								{
									xtype: 'tbtext',
									text: 'Amount'
								},
								{
									xtype: 'tbtext',
									id: 'Catalogue.toolbar.amount',
									text: ''
								},
								{
									xtype: 'tbseparator'
								},
								{
									xtype: 'tbtext',
									text: 'USD$'
								},
								{
									xtype: 'tbtext',
									id: 'Catalogue.toolbar.suma',
									text: ''
								}
							]
						}
					]
				}
			],
			dockedItems: [
				{
					xtype: 'toolbar',
					dock: 'top',
					items: [
						{
							xtype: 'tbseparator'
						},
						{
							xtype: 'tbtext',
							id: 'Catalogue.toolbar.text.username',
							text: document.username_
						},
						{
							xtype: 'textfield',
							id: 'Catalogue.toolbar.textfield.username',
							hidden: document.authorized,
							emptyText: 'Username'
						},
						{
							xtype: 'textfield',
							id: 'Catalogue.toolbar.textfield.password',
							hidden: document.authorized,
							inputType: 'password',
							emptyText: 'Password'
						},
						{
							xtype: 'button',
							text: 'Login',
							hidden: document.authorized,
							id: 'Catalogue.toolbar.textfield.login',
							handler: function() {
								username = Ext.getCmp('Catalogue.toolbar.textfield.username').getValue();
								password = Ext.getCmp('Catalogue.toolbar.textfield.password').getValue();
								
								Ext.Ajax.request({
									url: '/login',
									params: {
										username: username,
										password: password,
									},
									success: function(response){
										var text = response.responseText;
										if (text == '"ok"') {
											Ext.getCmp('Catalogue.toolbar.text.username').setText(Ext.getCmp('Catalogue.toolbar.textfield.username').getValue());
											
											Ext.getCmp('Catalogue.toolbar.textfield.username').hide();
											Ext.getCmp('Catalogue.toolbar.textfield.password').hide();
											Ext.getCmp('Catalogue.toolbar.textfield.login').hide();
											Ext.getCmp('Catalogue.toolbar.textfield.signin').hide();
											Ext.getCmp('Catalogue.toolbar.textfield.logout').show();
											
											Ext.getCmp('Catalogue.gridPanel.OrderStatus').setDisabled(false);
											Ext.getCmp('Catalogue.form').setDisabled(false);
											Ext.getCmp('Catalogue.gridPanel.Orders').getStore().load();
										}
									}
								});
							}
						},
						{
							xtype: 'button',
							text: 'Logout',
							hidden: !(document.authorized),
							id: 'Catalogue.toolbar.textfield.logout',
							handler: function() {
								Ext.Ajax.request({
									url: '/logout',
									success: function(response){
										var text = response.responseText;
										if (text == '"ok"') {
											Ext.getCmp('Catalogue.toolbar.text.username').setText('Guest');
											
											Ext.getCmp('Catalogue.toolbar.textfield.username').show();
											Ext.getCmp('Catalogue.toolbar.textfield.password').show();
											Ext.getCmp('Catalogue.toolbar.textfield.login').show();
											Ext.getCmp('Catalogue.toolbar.textfield.signin').show();
											Ext.getCmp('Catalogue.toolbar.textfield.logout').hide();
											
											Ext.getCmp('Catalogue.gridPanel.OrderStatus').setDisabled(true);
											Ext.getCmp('Catalogue.form').setDisabled(true);
											Ext.getCmp('Catalogue.gridPanel.Orders').getStore().load();
										}
									}
								});
							}
						},
						{
							xtype: 'button',
							text: 'Sign In',
							hidden: document.authorized,
							id: 'Catalogue.toolbar.textfield.signin',
							handler: function() {
								Ext.Ajax.request({
									url: '/signin',
									params: {
										'username': Ext.getCmp('Catalogue.toolbar.textfield.username').getValue(),
										'password': Ext.getCmp('Catalogue.toolbar.textfield.password').getValue()
									},
									success: function(response){
										var text = response.responseText;
										if (text == '"ok"') {
											Ext.getCmp('Catalogue.toolbar.text.username').setText('Registred');
											
											Ext.getCmp('Catalogue.toolbar.textfield.username').show();
											Ext.getCmp('Catalogue.toolbar.textfield.password').show();
										}
									}
								});
							}
						},
						{
							xtype: 'tbseparator'
						},
						{
							xtype: 'tbfill'
						},
						{
							xtype: 'tbseparator'
						}
					]
				}
			]
		});

		me.callParent(arguments);
	}

});
