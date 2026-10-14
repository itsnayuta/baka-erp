(()=>{frappe.templates.item_dashboard=`<div class="stock-levels">
	<div class="result">
	</div>
	<div class="more hidden" style="padding: 15px;">
		<a class="btn btn-default btn-xs btn-more">More</a>
	</div>
</div>
`;frappe.templates.item_dashboard_list=`{% for d in data %}
	<div class="dashboard-list-item">
		<div class="row">
			<div class="col-sm-3" style="margin-top: 8px;">
				<a data-type="warehouse" data-name="{{ d.warehouse }}">{{ d.warehouse }}</a>
			</div>
			<div class="col-sm-3" style="margin-top: 8px;">
				{% if show_item %}
					<a data-type="item"
						data-name="{{ d.item_code }}">{{ d.item_code }}
						{% if d.item_name != d.item_code %}({{ d.item_name }}){% endif %}
					</a>
				{% endif %}
			</div>
			<div class="col-sm-1" style="margin-top: 8px;" title="{{ __("Reserved Stock") }}">
				<a data-name="{{ d.reserved_stock }}">{{ d.reserved_stock }}</a>
			</div>
			<div class="col-sm-3">
				<span class="inline-graph">
					<span class="inline-graph-half" title="{{ __("Reserved Qty") }}">
						<span class="inline-graph-count">{{ d.total_reserved }}</span>
						<span class="inline-graph-bar">
							<span class="inline-graph-bar-inner"
								style="width: {{ cint(Math.abs(d.total_reserved)/max_count * 100) || 5 }}%">
							</span>
						</span>
					</span>
					<span class="inline-graph-half" title="{{ __("Actual Qty {0} / Waiting Qty {1}", [d.actual_qty, d.pending_qty]) }}">
						<span class="inline-graph-count">
							{{ d.actual_qty }} {{ (d.pending_qty > 0) ? ("(" + d.pending_qty+ ")") : "" }}
						</span>
						<span class="inline-graph-bar">
							<span class="inline-graph-bar-inner dark"
								style="width: {{ cint(d.actual_qty/max_count * 100) }}%">
							</span>
							{% if d.pending_qty > 0 %}
							<span class="inline-graph-bar-inner" title="{{ __("Projected Qty") }}"
								style="width: {{ cint(d.pending_qty/max_count * 100) }}%">
							</span>
							{% endif %}
						</span>
					</span>
				</span>
			</div>
			{% if can_write %}
			<div class="col-sm-2 text-right" style="margin: var(--margin-sm) 0;">
				{% if d.actual_qty %}
				<button class="btn btn-default btn-xs btn-move"
					data-disable_quick_entry="{{ d.disable_quick_entry }}"
					data-warehouse="{{ d.warehouse }}"
					data-actual_qty="{{ d.actual_qty }}"
					data-stock-uom="{{ d.stock_uom }}"
					data-item="{{ d.item_code }}">{{ __("Move") }}</button>
				{% endif %}
				<button style="margin-left: 7px;" class="btn btn-default btn-xs btn-add"
					data-disable_quick_entry="{{ d.disable_quick_entry }}"
					data-warehouse="{{ d.warehouse }}"
					data-actual_qty="{{ d.actual_qty }}"
					data-stock-uom="{{ d.stock_uom }}"
					data-item="{{ d.item_code }}"
					data-rate="{{ d.valuation_rate }}">{{ __("Add") }}</button>
			</div>
			{% endif %}
		</div>
	</div>
{% endfor %}
`;frappe.provide("erpnext.stock");erpnext.stock.ItemDashboard=class{constructor(e){$.extend(this,e),this.make()}make(){var e=this;this.start=0,this.sort_by||(this.sort_by="projected_qty",this.sort_order="asc"),this.content=$(frappe.render_template("item_dashboard")).appendTo(this.parent),this.result=this.content.find(".result"),this.content.on("click",".btn-move",function(){a($(this),"Move")}),this.content.on("click",".btn-add",function(){a($(this),"Add")}),this.content.on("click",".btn-edit",function(){let i=unescape($(this).attr("data-item")),s=unescape($(this).attr("data-warehouse")),n=unescape($(this).attr("data-company"));frappe.db.get_value("Putaway Rule",{item_code:i,warehouse:s,company:n},"name",t=>{frappe.set_route("Form","Putaway Rule",t.name)})});function a(i,s){let n=unescape(i.attr("data-item")),t=unescape(i.attr("data-warehouse")),o=unescape(i.attr("data-actual_qty")),c=Number(unescape(i.attr("data-disable_quick_entry"))),_=s==="Move"?"Material Transfer":"Material Receipt",l=unescape(i.attr("data-stock-uom"));if(c)r(n,t,_);else if(s==="Add"){let p=unescape($(this).attr("data-rate"));erpnext.stock.move_item(n,null,t,o,p,l,function(){e.refresh()})}else erpnext.stock.move_item(n,t,null,o,null,l,function(){e.refresh()})}function r(i,s,n){let t=n==="Material Transfer";erpnext.stock.make_stock_entry({item_code:i,source_warehouse:t?s:null,target_warehouse:t?null:s,stock_entry_type:n})}this.content.find(".btn-more").on("click",function(){e.start+=e.page_length,e.refresh()})}refresh(){this.before_refresh&&this.before_refresh();let e={item_code:this.item_code,warehouse:this.warehouse,parent_warehouse:this.parent_warehouse,item_group:this.item_group,company:this.company,start:this.start,sort_by:this.sort_by,sort_order:this.sort_order};var a=this;frappe.call({method:this.method,args:e,callback:function(r){a.render(r.message),a.after_refresh&&a.after_refresh()}})}render(e){this.start===0&&(this.max_count=0,this.result.empty());let a="";if(this.page_name==="warehouse-capacity-summary"?a=this.get_capacity_dashboard_data(e):a=this.get_item_dashboard_data(e,this.max_count,!0),e&&e.length===this.page_length+1?(this.content.find(".more").removeClass("hidden"),e.splice(-1)):this.content.find(".more").addClass("hidden"),a.data.length>0)this.content.find(".result").css("text-align","unset"),$(frappe.render_template(this.template,a)).appendTo(this.result);else{var r=__("No Stock Available Currently");this.content.find(".result").css("text-align","center"),$(`<div class='text-muted' style='margin: 20px 5px;'>
				${r} </div>`).appendTo(this.result)}}get_item_dashboard_data(e,a,r){a||(a=0),e||(e=[]),e.forEach(function(s){s.actual_or_pending=s.projected_qty+s.reserved_qty+s.reserved_qty_for_production+s.reserved_qty_for_sub_contract,s.pending_qty=0,s.total_reserved=s.reserved_qty+s.reserved_qty_for_production+s.reserved_qty_for_sub_contract,s.actual_or_pending>s.actual_qty&&(s.pending_qty=s.actual_or_pending-s.actual_qty),a=Math.max(s.actual_or_pending,s.actual_qty,s.total_reserved,a)});let i=0;return frappe.boot.user.can_write.indexOf("Stock Entry")>=0&&(i=1),{data:e,max_count:a,can_write:i,show_item:r||!1}}get_capacity_dashboard_data(e){e||(e=[]),e.forEach(function(r){r.color=r.percent_occupied>=80?"#f8814f":"#2490ef"});let a=0;return frappe.boot.user.can_write.indexOf("Putaway Rule")>=0&&(a=1),{data:e,can_write:a}}};erpnext.stock.move_item=function(d,e,a,r,i,s,n){var t=new frappe.ui.Dialog({title:a?__("Add Item"):__("Move Item"),fields:[{fieldname:"item_code",label:__("Item"),fieldtype:"Link",options:"Item",read_only:1},{fieldname:"source",label:__("Source Warehouse"),fieldtype:"Link",options:"Warehouse",read_only:1},{fieldname:"target",label:__("Target Warehouse"),fieldtype:"Link",options:"Warehouse",reqd:1,get_query(){return{filters:{is_group:0}}}},{fieldname:"qty",label:__("Quantity"),reqd:1,fieldtype:"Float",description:__("Available {0}",[r])},{fieldname:"rate",label:__("Rate"),fieldtype:"Currency",hidden:1}]});t.show(),t.get_field("item_code").set_input(d),e?t.get_field("source").set_input(e):(t.get_field("source").df.hidden=1,t.get_field("source").refresh()),i&&(t.get_field("rate").set_value(i),t.get_field("rate").df.hidden=0,t.get_field("rate").refresh()),a&&(t.get_field("target").df.read_only=1,t.get_field("target").value=a,t.get_field("target").refresh()),t.set_primary_action(__("Create Stock Entry"),function(){if(flt(t.get_value("qty"))<=0){frappe.msgprint(__("Quantity must be greater than zero"));return}if(e&&t.get_value("qty")>r){frappe.msgprint(__("Quantity must be less than or equal to {0}",[r]));return}if(t.get_value("source")===t.get_value("target")){frappe.msgprint(__("Source and target warehouse must be different"));return}erpnext.stock.make_stock_entry({item_code:t.get_value("item_code"),source_warehouse:t.get_value("source"),target_warehouse:t.get_value("target"),qty:t.get_value("qty"),rate:t.get_value("rate")})})};erpnext.stock.make_stock_entry=function(d){frappe.call({method:"erpnext.stock.dashboard.item_dashboard.make_stock_entry",args:d,freeze:!0,callback:e=>{let a=frappe.model.sync(e.message)[0];frappe.set_route("Form",a.doctype,a.name)}})};frappe.templates.warehouse_capacity_summary=`{% for d in data %}
	<div class="dashboard-list-item" style="padding: 7px 15px;">
		<div class="row">
			<div class="col-sm-2" style="margin-top: 8px;">
				<a data-type="warehouse" data-name="{{ d.warehouse }}">{{ d.warehouse }}</a>
			</div>
			<div class="col-sm-2" style="margin-top: 8px; ">
				<a data-type="item" data-name="{{ d.item_code }}">{{ d.item_code }}</a>
			</div>
			<div class="col-sm-1" style="margin-top: 8px; ">
				{{ d.stock_capacity }}
			</div>
			<div class="col-sm-2" style="margin-top: 8px; ">
				{{ d.actual_qty }}
			</div>
			<div class="col-sm-2">
				<div class="progress" title="Occupied Qty: {{ d.actual_qty }}" style="margin-bottom: 4px; height: 7px; margin-top: 14px;">
					<div class="progress-bar" role="progressbar"
						aria-valuenow="{{ d.percent_occupied }}"
						aria-valuemin="0" aria-valuemax="100"
						style="width:{{ d.percent_occupied }}%;
						background-color: {{ d.color }}">
					</div>
				</div>
			</div>
			<div class="col-sm-1" style="margin-top: 8px;">
				{{ d.percent_occupied }}%
			</div>
			{% if can_write %}
			<div class="col-sm-2 text-right" style="margin-top: 2px;">
				<button
					class="btn btn-default btn-xs btn-edit"
					style="margin: 4px 0; float: left;"
					data-warehouse="{{ d.warehouse }}"
					data-item="{{ d.item_code }}"
					data-company="{{ d.company }}">
					{{ __("Edit Capacity") }}
				</button>
			</div>
			{% endif %}
		</div>
	</div>
{% endfor %}
`;frappe.templates.warehouse_capacity_summary_header=`<div class="dashboard-list-item" style="padding: 12px 15px;">
	<div class="row">
		<div class="col-sm-2 text-muted" style="margin-top: 8px;">
			Warehouse
		</div>
		<div class="col-sm-2 text-muted" style="margin-top: 8px;">
			Item
		</div>
		<div class="col-sm-1 text-muted" style="margin-top: 8px;">
			Stock Capacity
		</div>
		<div class="col-sm-2 text-muted" style="margin-top: 8px;">
			Balance Stock Qty
		</div>
		<div class="col-sm-2 text-muted" style="margin-top: 8px;">
			% Occupied
		</div>
	</div>
</div>
`;})();
//# sourceMappingURL=item-dashboard.bundle.3JD6XTLP.js.map
