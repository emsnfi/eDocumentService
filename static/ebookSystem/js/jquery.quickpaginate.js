/* ===========================================================================
 *
 * JQuery Quick Pagination
 * Version 1.0.1
 * Quick and dirty pagination for pretty much any set of elements on the page.
 *
 * Author: Mark Perkins
 * Author email: mark@allmarkedup.com
 * For full documentation and more go to http://projects.allmarkedup.com/jquery_quick_paginate/
 *
 * ---------------------------------------------------------------------------
 *
 * LICENCE:
 *
 * Released under a MIT Licence. See licence.txt that should have been supplied with this file,
 * or visit http://projects.allmarkedup.com/jquery_quick_paginate/licence.txt
 *
 * ---------------------------------------------------------------------------
 * 
 * EXAMPLES OF USE:
 *
 * jQuery('.news_item').quickpaginate(); // would paginate all items on the page with the class of 'news_item'
 * 
 * jQuery('div#quick_slideshow img').quickpaginate(); // would paginate all img elements within the div with an id of 'quick_slideshow'
 *
 * // Paginate everything with the class of "news_item",
 * // 5 per 'page' and without the page counter.
 * jQuery('.news_item').quickpaginate( { perpage: 5, showcounter: false } ); 
 *
 * // Paginate all img elements and the element with the id of "info",
 * // with the prev/next/counter element appended to the element with the id of "pager_here"
 * jQuery('img, #info').quickpaginate({ pager : $("#pager_here") });
 *
 */

jQuery.fn.quickpaginate = function( settings ) {

	settings = jQuery.extend({
   
		perpage: 6,
		
		pager : null,
		
		showcounter : true,
		
		prev : "qp_next",

		next : "qp_prev",
		
		pagenumber : "qp_pagenumber",
		
		totalnumber : "qp_totalnumber",
		
		counter : "qp_counter"

	}, settings);

	var cm;
	
	var total;
	
	var last = false;
	
	var first = true;
	
	var items = jQuery(this);
	
	var nextbut;
	
	var prevbut;
	
	var init = function()
	{
		items.show();
		
		total = items.size();
				
		if ( items.size() > settings.perpage )
		{
			items.filter(":gt("+(settings.perpage-1)+")").hide();
			
			cm = settings.perpage;
			
			setNav();
		}
	};
	
	var goNext = function()
	{
		if ( !last )
		{
			var nm = cm + settings.perpage;
			items.hide();
			
			items.slice( cm, nm ).show();
			cm = nm;
			
			if ( cm >= total  )
			{
				last = true;
				nextbut.parent().addClass("disabled");
			}
			
			if ( settings.showcounter ) settings.pager.find("."+settings.pagenumber).text(cm/settings.perpage);
			
			prevbut.parent().removeClass("disabled");
			first = false;
		}
	};
	
	var goPrev = function()
	{
		if ( !first )
		{
			var nm = cm-settings.perpage;
			items.hide();
			
			items.slice( (nm - settings.perpage), nm ).show();
			cm = nm;
			
			if ( cm == settings.perpage  )
			{
				first = true;
				prevbut.parent().addClass("disabled");
			}
			
			if ( settings.showcounter ) settings.pager.find("."+settings.pagenumber).text(cm/settings.perpage);
			
			nextbut.parent().removeClass("disabled");
			last = false;
		}
	};
	
	var setNav = function()
	{
		if ( settings.pager === null )
		{	
			settings.pager = jQuery('<div style="text-align: center;"><ul id="doing_doc_list_counter" class="qc_pager pagination"></ul></div>');
			items.parent().parent().after(settings.pager);
		}
		
		var pagerNav = $('<li class="page-item"><a class="page-link ' + settings.prev + '" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span><span class="sr-only">Previous</span></a></li><li class="page-item"><a class="page-link ' + settings.next + '" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span><span class="sr-only">Next</span></a></li>');


		if (jQuery(settings.pager).find(".qc_pager").length > 0) {
		    jQuery(settings.pager).find(".qc_pager").append(pagerNav);
		} else {
		    jQuery(settings.pager).append(pagerNav);
		}
	
		if ( settings.showcounter )
		{
			var counter = '<span class="'+settings.counter+'"><span class="'+settings.pagenumber+'"></span> / <span class="'+settings.totalnumber+'"></span></span>';
			
			settings.pager.find("."+settings.prev).after( counter );
			
			settings.pager.find("."+settings.pagenumber).text( 1 );
			settings.pager.find("."+settings.totalnumber).text( Math.ceil(total / settings.perpage) );
		}

		nextbut = settings.pager.find("."+settings.next);
			
		prevbut = settings.pager.find("."+settings.prev);
		
		prevbut.parent().addClass("disabled");
		
		nextbut.click(function(){
			goNext();
			return false;
		});
		
		prevbut.click(function(){
			goPrev();
			return false;
		});
		
	};
	
	init(); // run the function
};



$(function(){
 		$('table').each( function() { 
 			if($(this).hasClass('no-page')==false)
 				$(this).find('tr').has('td').quickpaginate({ perpage: 10 }); 
 		} );
});