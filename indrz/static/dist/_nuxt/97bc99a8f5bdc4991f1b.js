(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{342:function(e,t,n){"use strict";var l=n(76),o=n.n(l),d=n(346),r=d.a.baseApiUrl;t.a={request:function(e){return o()({url:"".concat(e.url||r).concat(e.endPoint||""),method:e.method||"GET",headers:{Authorization:d.a.token,"Content-Type":"application/json"}})},getPageParams:function(e){var t=e.page,n=void 0===t?1:t,l=e.itemsPerPage,o=void 0===l?10:l;return{limit:o,offset:(n-1)*o}}}},346:function(e,t,n){"use strict";var l="https://navigatur.tuwien.ac.at",o=l+"/api/v1";t.a={baseApiUrl:o,defaultCenterXY:[1822252.75,6139984.7],baseWmsUrl:l+"/geoserver/wms",searchUrl:o+"/search",token:"Token 42519ebe7bada4d7a151c76832b94614ea5b198d",layerNamePrefix:"floor_",geoServerLayerPrefix:"indrztu:",defaultStartFloor:"eg"}},575:function(e,t,n){"use strict";n.r(t);n(10),n(8),n(4),n(7),n(3);var l=n(2),o=n(55),d=n(342),r={name:"AddEditShelf",props:{title:{type:String,default:function(){return""}},dialog:{type:Boolean,default:function(){return!1}},editedItem:{type:Object,default:function(){return{}}}},data:function(){return{loading:!1}},methods:{close:function(){this.$emit("close")},save:function(){var e=this;this.loading=!0,this.$store.dispatch("SAVE_SHELF",this.editedItem).then(function(t){e.$emit("save")}).catch(function(e){console.log(e)}).finally(function(){e.loading=!1})}}},c=n(33),m=n(37),f=n.n(m),v=n(139),h=n(423),_=n(343),x=n(562),I=n(318),y=n(563),S=n(473),k=n(118),O=n(561),w=n(321),j=n(455),component=Object(c.a)(r,function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-dialog",{attrs:{value:e.dialog,persistent:"","max-width":"500px"}},[n("v-card",[n("v-card-title",[n("span",{staticClass:"headline"},[e._v(e._s(e.title))])]),e._v(" "),n("v-card-text",[n("v-form",[n("v-container",[n("v-row",{attrs:{"no-gutters":""}},[n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"External Shelf ID"},model:{value:e.editedItem.bookshelf_id,callback:function(t){e.$set(e.editedItem,"bookshelf_id",t)},expression:"editedItem.bookshelf_id"}})],1),e._v(" "),n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"Floor Number"},model:{value:e.editedItem.floor,callback:function(t){e.$set(e.editedItem,"floor",t)},expression:"editedItem.floor"}})],1),e._v(" "),n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"External Shelf Section"},model:{value:e.editedItem.external_id,callback:function(t){e.$set(e.editedItem,"external_id",t)},expression:"editedItem.external_id"}})],1),e._v(" "),n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"Shelving System End Value"},model:{value:e.editedItem.system_to,callback:function(t){e.$set(e.editedItem,"system_to",t)},expression:"editedItem.system_to"}})],1),e._v(" "),n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"Shelving System Start Value"},model:{value:e.editedItem.system_from,callback:function(t){e.$set(e.editedItem,"system_from",t)},expression:"editedItem.system_from"}})],1),e._v(" "),n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"Left or Right Side"},model:{value:e.editedItem.side,callback:function(t){e.$set(e.editedItem,"side",t)},expression:"editedItem.side"}})],1),e._v(" "),n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"Distance From Measure"},model:{value:e.editedItem.measure_from,callback:function(t){e.$set(e.editedItem,"measure_from",t)},expression:"editedItem.measure_from"}})],1),e._v(" "),n("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[n("v-text-field",{attrs:{label:"Distance End Measure"},model:{value:e.editedItem.measure_to,callback:function(t){e.$set(e.editedItem,"measure_to",t)},expression:"editedItem.measure_to"}})],1)],1)],1)],1)],1),e._v(" "),n("v-card-actions",[n("v-spacer"),e._v(" "),n("v-btn",{attrs:{color:"blue darken-1",text:"",disabled:e.loading},on:{click:e.close}},[e._v("\n        Cancel\n      ")]),e._v(" "),n("v-btn",{attrs:{color:"blue darken-1",text:"",loading:e.loading,disabled:e.loading},on:{click:e.save}},[e._v("\n        Save\n        "),n("v-icon",{attrs:{right:""}},[e._v("\n          mdi-save\n        ")])],1)],1)],1)],1)},[],!1,null,"bd826d88",null),E=component.exports;function V(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);e&&(n=n.filter(function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable})),t.push.apply(t,n)}return t}function P(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?V(source,!0).forEach(function(t){Object(l.a)(e,t,source[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):V(source).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))})}return e}f()(component,{VBtn:v.a,VCard:h.a,VCardActions:_.a,VCardText:_.b,VCardTitle:_.c,VCol:x.a,VContainer:I.a,VDialog:y.a,VForm:S.a,VIcon:k.a,VRow:O.a,VSpacer:w.a,VTextField:j.a});var D={name:"ShelvesList",components:{AddEditShelf:E},data:function(){return{loading:!1,singleSelect:!1,dialog:!1,selected:[],pagination:{},headers:[{text:"External Id",align:"right",sortable:!1,value:"external_id"},{text:"System From",align:"right",sortable:!1,value:"system_from"},{text:"System To",align:"right",sortable:!1,value:"system_to"},{text:"Shelf Side",align:"right",sortable:!1,value:"side"},{text:"Map",value:"map",sortable:!1,width:"56px"},{text:"Edit",value:"edit",sortable:!1,width:"56px"}],editedIndex:-1,editedItem:{},defaultItem:{bookshelf_id:null,external_id:null,floor:null,id:null,measure_from:null,measure_to:null,section_child:null,section_id:null,section_main:null,side:"L",system_from:null,system_to:null}}},computed:P({},Object(o.c)({shelvesListData:function(e){var t=e.user.shelves,data=t.data,n=t.total;return this.total=n,data}}),{formTitle:function(){return-1===this.editedIndex?"New Shelf":"Edit Shelf"}}),watch:{dialog:function(e){e||this.close()},pagination:{handler:function(){this.loadData()},deep:!0}},mounted:function(){this.loadData()},methods:{loadData:function(){var e=this;this.loading||(this.loading=!0,this.$store.dispatch("user/LOAD_SHELVES",P({},d.a.getPageParams(this.pagination))).catch(function(e){console.log(e)}).finally(function(){e.loading=!1}))},editItem:function(e){this.editedIndex=this.shelvesListData.indexOf(e),this.editedItem=Object.assign({},e),this.dialog=!0},close:function(){var e=this;this.dialog=!1,setTimeout(function(){e.editedItem=Object.assign({},e.defaultItem),e.editedIndex=-1},300)},save:function(){this.editedIndex>-1&&Object.assign(this.shelvesListData[this.editedIndex],this.editedItem),this.close()}}},$=n(576),L=Object(c.a)(D,function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("v-data-table",{staticClass:"elevation-1",attrs:{headers:e.headers,items:e.shelvesListData,"server-items-length":e.total,"single-select":e.singleSelect,"item-key":"id",options:e.pagination,"show-select":"",loading:e.loading,"loading-text":"Loading... Please wait"},on:{"update:options":function(t){e.pagination=t}},scopedSlots:e._u([{key:"top",fn:function(){return[n("add-edit-shelf",{attrs:{title:e.formTitle,dialog:e.dialog,"edited-item":e.editedItem},on:{save:e.save,close:e.close}})]},proxy:!0},{key:"item.map",fn:function(t){t.item;return[n("v-icon",{attrs:{small:""}},[e._v("\n        mdi-map\n      ")])]}},{key:"item.edit",fn:function(t){var l=t.item;return[n("v-icon",{attrs:{small:""},on:{click:function(t){return e.editItem(l)}}},[e._v("\n        mdi-pencil\n      ")])]}}]),model:{value:e.selected,callback:function(t){e.selected=t},expression:"selected"}})],1)},[],!1,null,"61575966",null),C=L.exports;f()(L,{VDataTable:$.a,VIcon:k.a});var T={layout:"admin",components:{ShelvesList:C}},A=Object(c.a)(T,function(){var e=this.$createElement,t=this._self._c||e;return t("div",[t("shelves-list")],1)},[],!1,null,"097ab972",null);t.default=A.exports}}]);