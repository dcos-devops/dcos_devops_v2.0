function addhost(){
        context='<ul>'+
                        '<li>主机名:<input type="text" id="addhostname"></li>'+
                        '<li>主机IP:<input type="text" id="addhostip" onchange="checkip()"></li>'
        context += '<li>归属域:'+'<select id="addfields" class="form-control" onchange="getclusters()">'+
                   '</select>' + '</li>'
        context += '<li>归属约束:'+'<select id="addclusters" class="form-control">'+
                   '</select>' + '</li>'
        context += '<li>组件:'+'<select id="addcomponents" class="form-control">'+
                   '</select>' + '</li>'
        context += '<li>端口:<input type="text" id="addhostport"></li>'
        context +='</ul>'
        getfiels()
        getcomponent()
        var modalbody='table'
        modalbody=context
        $("#addhostbody").html(modalbody);
        $('#addhostmodal').modal('show');
}

function checkip(){
    addhostip=$('#addhostip').val()
    var exp1=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    var reg1=addhostip.match(exp1);
    if(reg1==null){
        alert('IP地址不合法！')
        return
    }
    $.get("/check_ip",{'ip': addhostip}, function (ret) {
            var checkres = ret.checkres;
            if (checkres.status==1){
                name=checkres.name
                field=checkres.field
                cluster=checkres.cluster
                addhostname=$('#addhostname').val(name)
                addfields=$('#addfields').val(field)
                getclusters()
            }
    })
}

function checkandaddhost(){
    addhostname=$('#addhostname').val()
    addhostip=$('#addhostip').val()
    addfields=$('#addfields').val()
    addclusters=$('#addclusters').val()
    addcomponents=$('#addcomponents').val()
    addhostport=$('#addhostport').val()
    var exp1=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    var reg1=addhostip.match(exp1);
    if(addhostname==''||addhostip==''||addfields=='--- 请选择生产域 ---'||addclusters=='--- 请选择集群约束 ---'||addclusters==''||addcomponents=='--- 请选择组件 ---'||addcomponents==''||addhostport=='')
    {
        alert('信息填写不完整！')
        return
    }
    if(reg1==null){
        alert('IP地址不合法！')
        return
    }
    var exp2=/^[1-9]\d{0,}$/
    var reg2=addhostport.match(exp2);
    if(reg2==null){
        alert('端口不合法！')
        return
    }
    $.get("/add_host",{'ip': addhostip,'field':addfields,'name':addhostname,'cluster':addclusters,'comp_name':addcomponents,'comp_port':addhostport}, function (ret) {
            var addres = ret.addres;
            if (addres.status==1){
                alert('添加成功！')
                $('#addhostmodal').modal('hide')
            }
            else{
                alert(addres.error)
            }
    })
}

function getfiels(){
    $.get("/search_field",{}, function (ret) {
            var fields = ret.fields;
            options='<option >--- 请选择生产域 ---</option>'
            for(var i = 0; i < fields.length; i++){
                options+='<option>'+fields[i]+'</option>'
            }
            $('#addfields').html(options)
        })
}

function getcomponent(){
    $.get("/get_component",{}, function (ret) {
            var components = ret.components;
            options='<option >--- 请选择组件 ---</option>'
            for(var i = 0; i < components.length; i++){
                options+='<option>'+components[i]+'</option>'
            }
            $('#addcomponents').html(options)
        })
}

function getclusters(){
    var x=document.getElementById("addfields");
    addfield=x.value
    $.get("/get_cluster", {'field': addfield}, function (ret) {
            var clusters = ret.clusters;
            options='<option >--- 请选择集群约束 ---</option>'
            for(var i = 0; i < clusters.length; i++){
                options+='<option>'+clusters[i]+'</option>'
            }
            $('#addclusters').html(options)
        })
}

function extractip(){
    var modallabel='主机ip';
    var modalbody='table'
    var ho=$(".select");
    hostips=new Array();
    hostnames=new Array();
    for(var i=0;i<ho.length;i++){
        if (ho[i].checked==true){
            hostip=$(ho[i].parentNode.parentNode.children[4]).html()
            hostips[i]=hostip
        }
    }
    context=
    '<table class="table table-bordered table-striped">'+
    '<thead>'+
        '<tr>'+
            '<td><b>主机IP</b></td>'+
        '</tr>'+
    '</thead>'+
    '<tbody>'
    for(var i=0;i<hostips.length;i++){
        context+=
        '<tr>'+
            '<td>'+hostips[i]+'</td>'+
        '</tr>'
    }
    // console.log(context)
    context+=
        '</tbody>'+
    '</table>'
    modalbody=context
    $("#clearlogslabel").text(modallabel);
    $("#clearlogsbody").html(modalbody);
    $('#clearlogsmodal').modal('show');
}

function rmdocker(dockerid){
    var r=confirm("确定要删除容器"+dockerid+"?");
    if (r==true)
    {
        $.get("/del_host_docker", {"hostip": hostip,"dockerid":dockerid}, function (ret) {
            var delres = ret.delres
            if(delres==dockerid){
                alert('删除了'+dockerid)
                showexitdocker(hostip)
            }
        });
    }
}

function cleanall(){
    hostip=$("#showdockerip").html()
    var r=confirm("确定要删除"+hostip+"所有退出容器?");
    if (r==true)
    {
        $.get("/clean_exit_dockers", {"hostip": hostip}, function (ret) {
            var delres = ret.delres
            alert('删除了:\n'+delres)
            showexitdocker(hostip)
        });
    }
}

function showexitdocker(hostip){
    context=
    '<table class="table table-bordered table-striped">'+
    '<thead>'+
        '<tr>'+
            '<td><b>ID</b></td>'+
            '<td><b>IMAGE</b></td>'+
            '<td><b>CREATED</b></td>'+
            '<td><b>STATUS</b></td>'+
            '<td>操作</td>'+
        '</tr>'+
    '</thead>'+
    '<tbody>'

    $.get("/search_host_exitdocker", {"hostip": hostip}, function (ret) {
        $("#showdockerbody").empty();
        var docker_infos = ret.docker_infos;

        console.log(docker_infos)


        for (var i = 0; i < docker_infos.length ; i++) {
            context += "<tr>" +
                "<td class='dockerid'>" + docker_infos[i]["ID"] + "</td>" +
                "<td>" + docker_infos[i]["IMAGE"] + "</td>" +
                "<td>" + docker_infos[i]["CREATED"] + "</td>" +
                "<td>" + docker_infos[i]["STATUS"] + "</td>" +
                '<td><button class="btn btn-danger" onclick="rmdocker('+"'"+docker_infos[i]["ID"]+"'"+')">删除容器</button></td>'+
                "</tr>";
        }

        context+="</tbody>"
        context+="</table>"
        $("#showdockerip").text(hostip);
        $("#showdockerbody").html(context);
        $('#showdockermodal').modal('show');
    });
}

function flashloglist(obj){
    line=$(obj).parents('tr')
    line.remove()
}

function delfile(obj){
    ip=$('#showlogip').html()
    filename=$(obj).parents('tr').find('.logfile').html()
    var r=confirm("确定要删除日志"+filename+"?");
    if (r==true)
    {
        $.get("/del_host_logfile", {"hostip": hostip,"filename":filename}, function (ret) {
            var delres = ret.delres
            console.log(delres)
            if(delres==''){
                alert('删除了'+filename)
                flashloglist(obj)
            }
        });
    }
}

function empty(obj){
    ip=$('#showlogip').html()
    filename=$(obj).parents('tr').find('.logfile').html()
    var r=confirm("确定要写空日志"+filename+"?");
    if (r==true)
    {
        $.get("/empty_host_logfile", {"hostip": hostip,"filename":filename}, function (ret) {
            var empres = ret.empres
            console.log(empres)
            console.log(filename)
            if(empres==''){
                alert('写空了'+filename)
                flashloglist(obj)
            }
            else{
                alert(empres)
            }
        });
    }
}

function showhostlogs(hostip){
    context=
    '<table class="table table-bordered table-striped">'+
    '<thead>'+
        '<tr>'+
            '<td><b>文件大小</b></td>'+
            '<td><b>文件位置</b></td>'+
            '<td>操作</td>'+
        '</tr>'+
    '</thead>'+
    '<tbody>'

    $.get("/search_host_logfile", {"hostip": hostip}, function (ret) {
        $("#showlogsbody").empty();
        var file_infos = ret.file_infos;

        console.log(file_infos)


        for (var i = 0; i < file_infos.length ; i++) {
            context += "<tr>" +
                "<td>" + file_infos[i]["size"] + "</td>" +
                "<td class='logfile'>" + file_infos[i]["filename"] + "</td>" +
                '<td><div class="btn-group">'+
                '<button class="btn btn-danger" onclick="delfile(this)">删除</button><button class="btn btn-warning" onclick="empty(this)">写空</button>'+
                "</div></td></tr>";
        }

        context+="</tbody>"
        context+="</table>"
        $("#showlogip").text(hostip);
        $("#showlogsbody").html(context);
        $('#showlogsmodal').modal('show');
    });
}

function cleanhosts(obj) {
    var modallabel='清理主机文件';
    var modalbody='table'
    var ho=$(".select");
    numofselect=0
    hostips=new Array();
    hostnames=new Array();
    for(var i=0;i<ho.length;i++){
        if (ho[i].checked==true){
            hostip=$(ho[i].parentNode.parentNode.children[4]).html()
            hostips[numofselect]=hostip
            hostname=$(ho[i].parentNode.parentNode.children[3]).html()
            hostnames[numofselect]=hostname
            numofselect=numofselect+1
        }
    }
    context=
    '<table class="table table-bordered table-striped">'+
    '<thead>'+
        '<tr>'+
            '<td><b>主机名</b></td>'+
            '<td><b>主机IP</b></td>'+
            '<td>清理日志文件</td>'+
            '<td>清理退出容器</td>'+
        '</tr>'+
    '</thead>'+
    '<tbody>'
    for(var i=0;i<hostips.length;i++){
        context+=
        '<tr>'+
            '<td>'+hostnames[i]+'</td>'+
            '<td>'+hostips[i]+'</td>'+
            "<td><a href='#' onclick='showhostlogs("+'"'+hostips[i]+'"'+")'>show logs</a></td>"+
            "<td><a href='#' onclick='showexitdocker("+'"'+hostips[i]+'"'+")'>show exit dockers</a></td>"+
        '</tr>'
    }
    // console.log(context)
    context+=
        '</tbody>'+
    '</table>'
    modalbody=context
    $("#clearlogslabel").text(modallabel);
    $("#clearlogsbody").html(modalbody);
    $('#clearlogsmodal').modal('show');
}
function changenum(){
    var ho=$(".select");
    numofselect=0
    for(var i=0;i<ho.length;i++){
        if (ho[i].checked==true){
            numofselect=numofselect+1
        }
    }
    $("#numofselect").html(numofselect)
}
function checkall(){
    var ho=$(".select");
    numofselect=0
    for(var i=0;i<ho.length;i++){
        ho[i].checked=true;
        numofselect=numofselect+1
    }
    $("#numofselect").html(numofselect)
}
function reverse(){
    var ho=$(".select");
    numofselect=0
    for(var i=0;i<ho.length;i++){
        ho[i].checked=!ho[i].checked;
        if (ho[i].checked==true){
            numofselect=numofselect+1
        }
    }
    $("#numofselect").html(numofselect)
}