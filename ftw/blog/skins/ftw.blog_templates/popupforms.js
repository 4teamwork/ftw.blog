/*jslint browser: true, white: false */
/*global jQuery */

/******
    Standard popups
******/

var common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';
var common_jqt_config = {fixed:false,speed:'fast',mask:{color:'#fff',opacity: 0.4,loadSpeed:0,closeSpeed:0}};

jQuery.extend(jQuery.tools.overlay.conf, common_jqt_config);

jQuery(function($){

    // method to show error message in a noform
    // situation.
    function noformerrorshow(el, noform) {
        var o = $(el),
            emsg = o.find('dl.portalMessage.error');
        if (emsg.length) {
            o.children().replaceWith(emsg);
            return false;
        } else {
            return noform;
        }
    }

    // After deletes we need to redirect to the target page.
    function redirectbasehref(el, responseText) {
        var mo = responseText.match(/<base href="(\S+?)"/i);
        if (mo.length === 2) {
            return mo[1];
        }
        return location;
    }

    // comment form
    $('form[name=reply]').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: '.enableAutoFocus',
            noform: function(el) {return noformerrorshow(el, 'redirect');},
            redirect: redirectbasehref
        }
    );

});

