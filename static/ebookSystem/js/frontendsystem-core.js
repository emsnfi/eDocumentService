﻿let comploader={}; //全域組件載入紀錄


function inicomp(name){
    //初始化組件
    let df = $.Deferred();

    //infor
    let o=inicomp_getinfor(name);

    //pre
    let dfs=[];
    if(o['pre'].length>0){
        for(let c of o['pre']){
            let s=inicomp(c);
            dfs.push(s);
        }
    }

    //each
    Promise.all(dfs)
    .then(function(){

        //core
        return inicomp_load(name);

    })
    .then(function(){
        df.resolve();
    })

    return df;
}


function inicomp_load(name){
    //載入組件
    let df = $.Deferred();

    if(haskey(comploader,name)){
        df.resolve();
    }
    else{
        let o=inicomp_getinfor(name);
        let timetag='?'+Date.now();
        timetag='';

        if(o['type']==='js'){
            $.getScript(o['url']+timetag)
            .done(function(){
                console.log('load: '+name+'['+o['type']+']')

                //true
                comploader[name]=true;

                df.resolve();
            })
        }
        else if(o['type']==='html'){
            $.get(o['url']+timetag)
            .done(function(h){
                console.log('load: '+name+'['+o['type']+']')

                //append
                $('body').append(h);

                //true
                comploader[name]=true;

                df.resolve();
            })
        }

    }

    return df;
}


function inicomp_getinfor(name){
    //取得組件資訊

    let o;
    if(name==='tinymce'){
        o={
            'url':'https://cdnjs.cloudflare.com/ajax/libs/tinymce/4.6.6/tinymce.min.js',
            'type':'js',
            'pre':[]
        }
    }
    else if(name==='wiriseditor'){
        o={
            'url':'/static/ebookSystem/js/wiriseditor/wiriseditor.js',
            'type':'js',
            'pre':[]
        }
    }
    else if(name==='mathjax'){
        o={
            'url':'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_SVG', //總套件62.9mb太大，直接用cdn
            'type':'js',
            'pre':[]
        }
    }
    else if(name==='mxeditor'){
        o={
            'url':'/static/ebookSystem/comp/mxeditor.html',
            'type':'html',
            'pre':['tinymce','wiriseditor','mathjax']
        }
    }
    else if(name==='mxdownloadbook'){
        o={
            'url':'/static/ebookSystem/comp/mxdownloadbook.html',
            'type':'html',
            'pre':[]
        }
    }

    return o;
}


function cint(v) {
    //轉整數

    if ($.isNumeric(v)) {
        return _.round(v);
    }

    return 0;
}


function cstr(v) {
    //轉字串

    return String(v);
}


function isundefined(v) {
    //判斷是否為undefined

    let c = Object.prototype.toString.call(v);
    return c === '[object Undefined]';
}


function isnull(v) {
    //判斷是否為null

    let c = Object.prototype.toString.call(v);
    return c === '[object Null]';
}


function isempty(v) {
    //判斷是否為空物件

    if (isobj(v)) {
        for (let k in v) {
            return false;
        }
        return true;
    }
    return false;
}


function iszerolength(v) {
    //判斷是否為無內容陣列

    if (isarr(v)) {
        if (v.length === 0) {
            return true;
        }
        return false;
    }
    return false;
}


function isnothing(v) {
    //判斷是否為空字串

    if (v === '') {
        return true;
    }
    return false;
}


function iser(v) {
    //判斷是否為泛用無效

    if (isundefined(v)) {
        return true;
    }
    if (isnull(v)) {
        return true;
    }
    if (isempty(v)) {
        return true;
    }
    if (isnothing(v)) {
        return true;
    }
    if (iszerolength(v)) {
        return true;
    }
    return false;
}


function iselmexist(id) {
    //判斷元素是否存在

    return !(document.getElementById(id) === null);
}


function iscontainaz09(c) {
    //判斷字串是否包含英文與數字

    let reg = /^[A-Za-z0-9]+$/;
    return reg.test(c);
}


function isarr(v) {
    //判斷是否為陣列

    let c = Object.prototype.toString.call(v);
    return c === '[object Array]';
}


function isfun(v) {
    //判斷是否為函數

    let c = Object.prototype.toString.call(v);
    return c === '[object Function]';
}


function isnum(v) {
    //判斷是否為數字

    return $.isNumeric(v);
}


function isstr(v) {
    //判斷是否為字串

    let c = Object.prototype.toString.call(v);
    return c === '[object String]';
}


function isobj(v) {
    //判斷是否為物件

    let c = Object.prototype.toString.call(v);
    return c === '[object Object]';
}


function binstr(s, ins) {
    //判斷字串s是否「包含、出現」任一字串陣列ins內元素

    if (!isstr(s)){
        return false;
    }

    //instr
    function instr(s, ins) {
        return s.indexOf(ins);
    }

    //不是陣列則自動轉陣列
    if (!isarr(ins)) {
        ins = [ins];
    }

    //判斷是否包含ins元素
    for (let k in ins) {
        let v = ins[k];
        if (instr(s, v) !== -1) {
            return true;
        }
    }

    return false;
}


function arrhas(ltar, ltcontain) {
    //判斷任一字串陣列ltar內元素，是否「等於」任一字串陣列ltcontain內元素

    //不是陣列則自動轉陣列
    if (isstr(ltar)) {
        ltar = [ltar];
    }
    else if (isarr(ltar)) {
        //預設輸入陣列
    }
    else {
        return false;
    }

    //不是陣列則自動轉陣列
    if (isstr(ltcontain)) {
        ltcontain = [ltcontain];
    }
    else if (isarr(ltcontain)) {
        //預設輸入陣列
    }
    else {
        return false;
    }

    //由ltar各元素當中，若存在ltcontain內任一元素則回傳true，反之回傳false
    for (let i = 0; i < ltar.length; i++) {
        for (let j = 0; j < ltcontain.length; j++) {
            if (ltar[i] === ltcontain[j]) {
                return true;
            }
        }
    }
    return false;
}


function haskey(obj, key) {
    //判斷物件是否有key屬性

    if (!isobj(obj)) {
        return false;
    }
    return (key in obj);
}


function o2j(v) {
    //物件轉json文字

    let c = '';
    try {
        c = JSON.stringify(v);
        //c = JSON.stringify(v, null, '\t');
    }
    catch (err) {
    }

    return c;
}


function j2o(v) {
    //json文字轉物件

    let c = {};
    try {
        c = JSON.parse(v);
    }
    catch (err) {
    }

    return c;
}


function utoa(str) {
    //任意字串轉base64字串

    //btoa
    let r = window.btoa(unescape(encodeURIComponent(str)));

    return r;
}


function atou(str) {
    //base64字串轉任意字串

    //atob
    let r = decodeURIComponent(escape(window.atob(str)));

    return r;
}


function o2b(obj) {
    //物件轉base64字串

    let r = '';
    try {
        r = utoa(o2j(obj));
    }
    catch (err) {
    }

    return r;
}


function b2o(str) {
    //base64字串轉物件

    let r = {};
    try {
        r = j2o(atou(str));
    }
    catch (err) {
    }

    return r;
}


function GenID() {
    let p = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let c = "";
    let n = 32;
    for (let i = 0; i < n; i++) {
       c += p.charAt(Math.floor(Math.random() * p.length));
    }
    return c;
    //return Math.uuid(32);
}


function downloadfile(cfn, bindata) {
	//下載binary資料成為檔案
	//使用標籤a與blob物件直接將bindata下載成為檔案

	//tag a
	let downloadLink = document.createElement('a');
	let blob = new Blob([bindata]);
	let url = URL.createObjectURL(blob);
	downloadLink.href = url;
	downloadLink.download = cfn;

	//download
	document.body.appendChild(downloadLink);
	downloadLink.click();
	document.body.removeChild(downloadLink);

}


function alertDialog(json) {
    //原ajaxSubmit.js的alertDialog
    
    var str=(json.status=='error')?'danger':'success'
    var dialog='#'+str+'Dialog';
    $(dialog+" .alertMessage").html(json.message);
    $(dialog).on('shown.bs.modal', function () {
        $(dialog+" .close").focus();
    });
    $(dialog).modal();
    $(dialog).on('hide.bs.modal', function () {
        if(json.hasOwnProperty('redirect_to'))
            window.location.href = json.redirect_to; 
        else
            if(json.status!='error')
                location.reload();
    });
}


function alertok(msg){
    //alertDialog顯示ok訊息, 需引用utils/dialog.html

    let json={};
    json.status='success';
    json.message=msg;
    alertDialog(json);
}


function alerterr(msg){
    //alertDialog顯示error訊息, 需引用utils/dialog.html

    let json={};
    json.status='error';
    json.message=msg;
    alertDialog(json);
}


function pagetab_initial(data){
    //產生分頁

    let c='';
    c+='<ul class="nav nav-tabs">';

    //each li
    _.each(data,function(v,k){
        c+='<li><a href="#'+v['id']+'" name="'+v['name']+'" prop="'+v['prop']+'" data-toggle="tab">'+v['title']+'</a></li>';
    })
    
    c+='</ul>';
	
    c+='<div class="tab-content">';

    //each div
    _.each(data,function(v,k){
        c+='<div id="'+v['id']+'" class="tab-pane" style="margin:20px;"></div>';
    })
    
    c+='</div>';

    return c;
}


function pagin_initial(tabid){
    //添加表格分頁功能

    //tab
    let tab=$('#'+tabid);

    //trs
    let trs=tab.find('tbody').find('tr');

    //numrow
    let numrow=trs.length;

    //numperpage
    let numperpage=10;

    //numpage
    let numpage=Math.ceil(numrow/numperpage);

    let c='';
    c+='<div style="text-align:center;">';
    c+='<ul id="'+tabid+'_pagination" class="pagination" style="margin:0px;" tabid="'+tabid+'" pagenow="1" numrow="'+numrow+'" numperpage="'+numperpage+'" numpage="'+numpage+'">';
    c+='<li class="prev" style="cursor:pointer;"><a onclick="pagin_change(\''+tabid+'\',\'-1\')">«</a></li>';
    c+='<li class=""><a >1 / '+numpage+'</a></li>';
    c+='<li class="next" style="cursor:pointer;"><a onclick="pagin_change(\''+tabid+'\',\'+1\')">»</a></li>';
    c+='</ul>';
    c+='</div>';
    
    //after
    tab.after(c);

    //change
    pagin_change(tabid,1)

}


function pagin_change(tabid,oper){
    //表格分頁切換

    let tab=$('#'+tabid);
    let pag=$('#'+tabid+'_pagination');
    let pagenow=cint(pag.attr('pagenow'));
    let numperpage=cint(pag.attr('numperpage'));
    let numpage=cint(pag.attr('numpage'));

    //pagenow
    if(String(oper)==='+1'){
        pagenow+=1;
    }
    else if(String(oper)==='-1'){
        pagenow-=1;
    }
    else{
        pagenow=cint(oper);
    }

    //check
    pagenow=Math.max(pagenow,1);
    pagenow=Math.min(pagenow,numpage);

    //save
    pag.attr('pagenow',pagenow);

    //show
    pag.find('li').eq(1).find('a').html(pagenow+' / '+numpage);

    //trs
    let trs=tab.find('tbody').find('tr');
    
    //each
    trs.each(function(i){
        let tr=$(this);
        let j=i+1;
        if( j >= numperpage*(pagenow-1)+1 && j <= numperpage*(pagenow)){
            tr.show();
        }
        else{
            tr.hide();
        }
    })

}


function aj_get(url, transferData){
    //ajax get

    return aj_send('get', url, transferData);
}


function aj_post(url, transferData){
    //ajax post

    return aj_send('post', url, transferData);
}


function aj_send(type, url, transferData){
    //ajax

    return $.ajax({
        url:url,
        type: type,
        data: transferData,
        beforeSend:function(jqXHR, settings){
            let csrf=$('input[name=csrfmiddlewaretoken]').val();
            jqXHR.setRequestHeader('X-CSRFToken', csrf);
            jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        }
    });
}


function aj_binary(url, transferData){
    //console.log(url)

    //getdisposition
    function getdisposition(xhr){
        let filename='';
        let disposition = xhr.getResponseHeader('Content-Disposition');
        if (disposition && disposition.indexOf('attachment') !== -1) {
            let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            let matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }
        }
        return filename;
    }

    return $.ajax({
        url:url,
        type: "POST",
        data: transferData,
        dataType: "binary",
        beforeSend:function(jqXHR, settings){
            let csrf=$('input[name=csrfmiddlewaretoken]').val();
            jqXHR.setRequestHeader('X-CSRFToken', csrf);
            jqXHR.setRequestHeader("X-Requested-With", "XMLHttpRequest")
        },
        success: function(bdata,status,xhr){
            //console.log(bdata);

            if(bdata.type==='application/octet-stream'){
                let filename=getdisposition(xhr);
                downloadfile(filename, bdata);
            }
            else{
                alerterr('密碼錯誤或準備文件失敗');
            }

        },
        error:function(xhr,errmsg,err){
            //console.log(xhr.responseText);
            alerterr('密碼錯誤或準備文件失敗');
        }
    });
}


function aj_booklist(query_type, query_value){
    //API使用book_list查找書籍資訊

    //df
    let df = $.Deferred();

    //url
    let url='/ebookSystem/book_list';

    //transferData
    let transferData={
        'query_type':query_type,
        'query_value':query_value
    };

    //aj_get
    aj_get(url,transferData)
    .done(function(data){
        
        if(data['status']==='success'){

            //o
            let o=data['content']['book'];

            //p
            let p=[];
            _.each(o, function(v,k){
                p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
                // p.push(v[1]);
            })

            if(p.length>0){
                df.resolve(p);
            }
            else{
                df.reject('查無書籍資料');
            }
        
        }
        else{
            console.log(data['message']);
            df.reject('查無書籍資料');
        }

    })
    .fail(function(msg){
        console.log(msg)
        df.reject('查無書籍資料');
    })
    
    return df;
}