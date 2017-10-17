function addhost(){
        context='<ul>'+
                        '<li>主机名:<input type="text" ></li>'+
                        '<li>主机IP:<input type="password" ></li>'
        context += '<li>归属域:'+'<select id="fields" name="fields" class="form-control">'+
                        '<option >--- 请选择生产域 ---</option>' +
                            '<option>内网(DCOS)</option>' +
                            '<option>DMZ</option>' +
                            '<option>DCOS 3.0</option>' +
                            '<option>内网(非DCOS)</option>' +
                   '</select>' + '</li>'
        context += '<li>归属约束:'+'<select id="fields" name="fields" class="form-control">'+
                        '<option >--- 请选择集群约束 ---</option>' +
                            '<option>无</option>' +
                            '<option>dcos:center-n</option>' +
                            '<option>dcos:center-d</option>' +
                            '<option>dcos:LITTLEAPP</option>' +
                            '<option>centering:sd</option>' +
                            '<option>centering:sq</option>' +
                            '<option>dcos:XYL-DISHI</option>' +
                            '<option>dcos:DMZ-XYL</option>' +
                   '</select>' + '</li>'
        context +='</ul>'
        var modalbody='table'
        modalbody=context
        console.log(context)
        $("#addhostbody").html(modalbody);
        $('#addhostmodal').modal('show');
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