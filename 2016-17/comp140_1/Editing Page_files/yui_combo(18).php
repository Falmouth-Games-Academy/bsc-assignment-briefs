/*
YUI 3.15.0 (build 834026e)
Copyright 2014 Yahoo! Inc. All rights reserved.
Licensed under the BSD License.
http://yuilibrary.com/license/
*/

YUI.add("resize-plugin",function(e,t){var n=function(t){t.node=e.Widget&&t.host instanceof e.Widget?t.host.get("boundingBox"):t.host,t.host instanceof e.Widget?t.widget=t.host:t.widget=!1,n.superclass.constructor.call(this,t)};n.NAME="resize-plugin",n.NS="resize",n.ATTRS={node:{value:undefined},widget:{value:undefined}},e.extend(n,e.Resize,{initializer:function(e){this.set("node",e.node),this.set("widget",e.widget),this.on("resize:resize",function(e){this._correctDimensions(e)})},_correctDimensions:function(e){var t=this.get("node"),n={old:t.getX(),cur:e.currentTarget.info.left},r={old:t.getY(),cur:e.currentTarget.info.top};this.get("widget")&&this._setWidgetProperties(e,n,r),this._isDifferent(n.old,n.cur)&&t.set("x",n.cur),this._isDifferent(r.old,r.cur)&&t.set("y",r.cur)},_setWidgetProperties:function(t,n,r){var i=this.get("widget"),s=i.get("height"),o=i.get("width"),u=t.currentTarget.info.offsetWidth-t.currentTarget.totalHSurrounding,a=t.currentTarget.info.offsetHeight-t.currentTarget.totalVSurrounding;this._isDifferent(s,a)&&i.set("height",a),this._isDifferent(o,u)&&i.set("width",u),i.hasImpl&&i.hasImpl(e.WidgetPosition)&&(this._isDifferent(i.get("x"),n.cur)&&i.set("x",n.cur),this._isDifferent(i.get("y"),r.cur)&&i.set("y",r.cur))},_isDifferent:function(e,t){var n=!1;return e!==t&&(n=t),n}}),e.namespace("Plugin"),e.Plugin.Resize=n},"3.15.0",{requires:["resize-base","plugin"],optional:["resize-constrain"]});

// Incorrect moodle module inclusion. Not enough component information in m/1462863939/core_filepicker/core_filepicker.js.
/*
YUI 3.15.0 (build 834026e)
Copyright 2014 Yahoo! Inc. All rights reserved.
Licensed under the BSD License.
http://yuilibrary.com/license/
*/

YUI.add("intl",function(e,t){var n={},r="yuiRootLang",i="yuiActiveLang",s=[];e.mix(e.namespace("Intl"),{_mod:function(e){return n[e]||(n[e]={}),n[e]},setLang:function(e,t){var n=this._mod(e),s=n[i],o=!!n[t];return o&&t!==s&&(n[i]=t,this.fire("intl:langChange",{module:e,prevVal:s,newVal:t===r?"":t})),o},getLang:function(e){var t=this._mod(e)[i];return t===r?"":t},add:function(e,t,n){t=t||r,this._mod(e)[t]=n,this.setLang(e,t)},get:function(t,n,r){var s=this._mod(t),o;return r=r||s[i],o=s[r]||{},n?o[n]:e.merge(o)},getAvailableLangs:function(t){var n=e.Env._loader,r=n&&n.moduleInfo[t],i=r&&r.lang;return i?i.concat():s}}),e.augment(e.Intl,e.EventTarget),e.Intl.publish("intl:langChange",{emitFacade:!0})},"3.15.0",{requires:["intl-base","event-custom"]});
/*
YUI 3.15.0 (build 834026e)
Copyright 2014 Yahoo! Inc. All rights reserved.
Licensed under the BSD License.
http://yuilibrary.com/license/
*/

YUI.add("lang/datatable-message_en",function(e){e.Intl.add("datatable-message","en",{emptyMessage:"No data to display",loadingMessage:"Loading..."})},"3.15.0");
/*
YUI 3.15.0 (build 834026e)
Copyright 2014 Yahoo! Inc. All rights reserved.
Licensed under the BSD License.
http://yuilibrary.com/license/
*/

YUI.add("lang/datatable-sort_en",function(e){e.Intl.add("datatable-sort","en",{asc:"Ascending",desc:"Descending",sortBy:"Sort by {column}",reverseSortBy:"Reverse sort by {column}"})},"3.15.0");
